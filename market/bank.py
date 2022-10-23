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
    def account_id(self):
        return self._account_id

    def credit_balance(self):
        if self._credit:
            return self._credit.balance
        else:
            return 0

    def available_credit(self):
        if self._credit:
            return self._credit.limit + self._credit.balance
        else:
            return 0

    def credit(self, amount):
        if self._credit:
            return self._credit.credit(amount)

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
    actor_id: uuid.uuid4
    account_names: dict[str, uuid.uuid4]
    _accounts: dict[uuid.uuid4, Account]
    _debt: dict[uuid.uuid4, Debt]
    _balance: float

    @property
    def balance(self):
        return sum(account.balance for account in self._accounts)

    def add_account(self, account: Account):
        pass

    def add_debt(self, debt: Debt):
        pass

    def account_exist(self, account_id: uuid.uuid4 = None, account_name: str = None):
        pass


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
