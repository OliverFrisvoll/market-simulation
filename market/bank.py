import uuid
import time
import datetime
import numpy as np
from dataclasses import dataclass


class Debt:
    def __init__(self, amount: float, debt_type: str, interest_rate: float, actor_id: uuid.uuid4,
                 creditor_id: uuid.uuid4):
        self.debt_id = uuid.uuid4()
        self._actor_id: uuid.uuid4 = actor_id
        self._creditor_id: uuid.uuid4 = creditor_id
        self._amount: float = amount
        self._debt_type: str = debt_type
        self._interest: float = interest_rate
        self.time_since_interest = datetime.datetime.now()

    @property
    def amount(self):
        return self._amount

    def calculate_interest(self):
        interval = (now := datetime.datetime.now()) - self.time_since_interest
        self.time_since_interest = now
        interest = np.power(self._interest, interval.days / 365)
        self._amount = self._amount * interest
        return interest - 1

    def balance(self):
        self.calculate_interest()
        return self._amount

    def repay_all(self):
        self.calculate_interest()
        payable = self._amount
        self._amount = 0
        return payable

    def repay(self, amount):
        self.calculate_interest()
        if amount < 0:
            raise ValueError("Cannot repay negative amount")
        net = self._amount - amount
        if net < 0:
            self._amount = 0
            return True, net
        elif net == 0:
            self._amount = 0
            return True, 0

        else:
            self._amount -= amount
            return False, net


@dataclass
class Credit:
    _limit: int
    _balance: int = 0
    # Add an interest rate implementation
    interest_rate: float = None

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, amount):
        if amount < 0:
            raise ValueError("Cannot set negative limit")
        self._limit = amount

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    def credit(self, amount):
        if amount > 0:
            self.balance += amount
            return True, self.limit + self.balance
        elif amount < 0:
            if (self.limit + self.balance) >= abs(amount):
                self.balance += amount
                return True, self.limit + self.balance
            else:
                return False, self.limit + self.balance
        else:
            return True, self.limit + self.balance


class Account:
    def __init__(self, account_name: str, balance: float, credit: Credit = None):
        self._account_name: str = account_name
        self._account_id: uuid.uuid4 = uuid.uuid4()
        self._balance: float = balance
        self._credit: Credit = credit

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        self._balance = amount

    @property
    def account_name(self):
        return self._account_name

    @property
    def account_id(self):
        return self._account_id

    def credit_balance(self):
        if self._credit:
            return self._credit.balance
        else:
            return False, 0

    def available_credit(self):
        if self._credit:
            return self._credit.limit + self._credit.balance
        else:
            return False, 0

    def credit(self, amount):
        if self._credit:
            return self._credit.credit(amount)

    def credit_limit(self):
        if self._credit:
            return self._credit.limit
        else:
            return False, 0

    def change_limit(self, limit):
        if self._credit:
            self._credit._limit = limit
            return True, self._credit.limit
        else:
            return False, 0

    def withdraw(self, amount):
        if amount > 0:
            if self.balance - amount >= 0:
                self.balance = self.balance - amount
                return True, self.balance
            elif self.available_credit() >= abs(rest := self.balance - amount):
                self.balance = 0
                self.credit(rest)
                return True, self.balance
            else:
                return False, self.balance
        else:
            return False, self.balance

    def deposit(self, amount):
        if amount > 0:
            self.balance = self.balance + amount
            return True, self.balance
        else:
            return False, self.balance


class AccountHolder:
    def __init__(self, actor_id: uuid.uuid4, ):
        self.actor_id: uuid.uuid4 = actor_id
        self._account_names: dict[str, uuid.uuid4] = {}
        self._accounts: dict[uuid.uuid4, Account] = {}
        self._debt: dict[uuid.uuid4, Debt] = {}
        self._balance: float = 0

    @property
    def balance(self):
        if self._accounts:
            return sum(account.balance for account in self._accounts)

    def accounts(self):
        return self._account_names.keys()

    def account_balance(self, account):
        account = self.get_account(account)
        return account.balance if account else None

    def get_account(self, account):
        if isinstance(account, str):
            account = self._accounts.get(self._account_names.get(account, None), None)
        else:
            account = self._accounts.get(account, None)
        return account

    def add_account(self, account_name: str, balance: float, credit: Credit = None):
        if account_name not in self._account_names:
            account = Account(account_name, balance, credit)
            self._accounts[account.account_id] = account
            self._account_names[account_name] = account.account_id
            return True, account.account_id
        else:
            return False, None

    def del_account(self, account):
        account = self.get_account(account)
        if account:
            self._account_names.pop(account.account_name)
            self._accounts.pop(account.account_id)
            return True, account.balance - account.credit_balance()
        else:
            return False, None

    def debt_balance(self):
        return sum(debt.balance() for debt in self._debt.values())

    def add_debt(self, account, debt: Debt):
        account = self.get_account(account)
        if account:
            account.deposit(debt.amount)
            self._debt[debt.debt_id] = debt
            return True, debt.debt_id
        else:
            return False, None

    def pay_debt(self, amount, account, debt_id=None):
        account = self.get_account(account)
        if account.balance >= amount:
            if debt_id:
                debt = self._debt.get(debt_id, None)
                if debt:
                    paid, net = debt.repay(amount)
                    if paid:
                        if net < 0:
                            amount += net
                        account.withdraw(amount)
                        self._debt.pop(debt_id)
                    else:
                        account.withdraw(amount)
                    return True, amount
                else:
                    return False, None
            else:
                total_amount = amount
                for _, debt in self._debt.values():
                    paid, net = debt.repay(amount)
                    if paid:
                        amount += net
                        self._debt.pop(debt_id)
                    else:
                        account.withdraw(amount)
                        return True, None

    def del_debt(self, account, debt_id):
        account = self.get_account(account)
        debt = self._debt.get(debt_id, None)
        if debt:
            amount = debt.balance()
            if account.balance >= amount:
                account.withdraw(amount)
                status, paid = self.pay_debt(amount, account.account_id, debt_id)
                return True, 0
            else:
                return False, account.balance - amount
        else:
            return False, None

    def credit(self, account):
        account = self.get_account(account)
        return account.credit_balance() if account else None

    def available_credit(self, account):
        account = self.get_account(account)
        return account.available_credit() if account else None

    def credit_limit(self, account):
        account = self.get_account(account)
        return account.credit_limit() if account else None

    def total_credit(self):
        return sum(account.credit_balance() for account in self._accounts.values())

    def total_available_credit(self):
        return sum(account.available_credit() for account in self._accounts.values())

    def change_credit_limit(self, account, limit):
        account = self.get_account(account)
        if account:
            return account.credit.change_limit(limit)
        else:
            return False, None


class Bank:
    def __init__(self):
        self.bank_id = uuid.uuid4()


class PrivateBank(Bank):
    def __init__(self):
        super().__init__()
        self._issued_debt: dict
        self._accounts: dict

    def create_account(self, actor_id: uuid.uuid4, account_name: str, balance: float):
        pass
