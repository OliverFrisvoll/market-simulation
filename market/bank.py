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
        self._amount = self._amount + interest
        return interest

    def balance_left(self):
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
            return False, net


@dataclass
class Credit:
    pass


@dataclass
class Account:
    account_id: uuid.uuid4
    account_name: str
    balance: float


class PrivateBank:
    def __init__(self):
        self._accounts: dict[uuid.uuid4, Account]

    def create_account(self, actor_id: uuid.uuid4, account_name: str, balance: float):
        pass
