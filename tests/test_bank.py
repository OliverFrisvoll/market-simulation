import unittest
import uuid
from bank import Debt, Credit, Account, AccountHolder, Bank


class TestDebt(unittest.TestCase):
    def test_calculate_interest_zero(self):
        actor_id = uuid.uuid4()
        creditor_id = uuid.uuid4()
        debt = Debt(100, "loan", 0, actor_id, creditor_id)
        self.assertEqual(debt.calculate_interest(), 0, "Interest should be 0")

    def test_balance(self):
        actor_id = uuid.uuid4()
        creditor_id = uuid.uuid4()
        debt = Debt(100, "loan", 0, actor_id, creditor_id)
        self.assertEqual(debt.balance(), 100, "Balance should be 100")

    def test_repay(self):
        actor_id = uuid.uuid4()
        creditor_id = uuid.uuid4()
        debt = Debt(100, "loan", 0, actor_id, creditor_id)
        self.assertEqual(debt.repay(50), (False, 50), "Repay should return False, 50")
        self.assertEqual(debt.balance(), 50, "Balance should be 50")
        self.assertEqual(debt.repay(50), (True, 0), "Repay should return True, 0")
        debt = Debt(100, "loan", 0, actor_id, creditor_id)
        self.assertEqual(debt.repay(100), (True, 0), "Repay should return True, 0")

    def test_repay_all(self):
        actor_id = uuid.uuid4()
        creditor_id = uuid.uuid4()
        debt = Debt(100, "loan", 0, actor_id, creditor_id)
        self.assertEqual(debt.repay_all(), 100, "Repay should return 100")
        self.assertEqual(debt.balance(), 0, "Balance should be 0")


class TestCredit(unittest.TestCase):
    def test_use_credit(self):
        credit = Credit(100, 0, 0)
        self.assertEqual(credit.credit(-50), (True, 50), "Use credit should return True")
        self.assertEqual(credit.credit(-50), (True, 0), "Use credit should return True")
        self.assertEqual(credit.credit(-1), (False, 0), "Use credit should return False")
        credit.credit(10)
        self.assertEqual(credit.credit(-11), (False, 10), "Use credit should return False")

    def test_credit_limit(self):
        credit = Credit(100, 0, 0)
        self.assertEqual(credit.credit(-100), (True, 0), "Use credit should return True")
        self.assertEqual(credit.credit(-1), (False, 0), "Use credit should return False")

    def test_repay_credit(self):
        credit = Credit(100, 0, 0)
        credit.credit(-50)
        self.assertEqual(credit.credit(50), (True, 100), "Repay credit should return True, 0")


class TestAccount(unittest.TestCase):
    def test_balance(self):
        account = Account("name", 100)
        self.assertEqual(account.balance, 100, "Balance should be 100")
        self.assertEqual(account.deposit(50), (True, 150), "Deposit should return True, 150")
        self.assertEqual(account.balance, 150, "Balance should be 150")
        self.assertEqual(account.withdraw(50), (True, 100), "Withdraw should return True, 100")
        self.assertEqual(account.withdraw(101), (False, 100), "Withdraw should return False, 100")
        self.assertEqual(account.withdraw(-1), (False, 100), "Withdraw should return False, 100")
        self.assertEqual(account.deposit(-1), (False, 100), "Deposit should return False, 100")
        self.assertEqual(account.balance, 100, "Balance should be 100")

    def test_balance_with_credit(self):
        account = Account("name", 100, Credit(100, 0, 0))
        self.assertEqual(account.balance, 100, "Balance should be 100")
        self.assertEqual(account.deposit(50), (True, 150), "Deposit should return True, 150")
        self.assertEqual(account.balance, 150, "Balance should be 150")
        self.assertEqual(account.withdraw(50), (True, 100), "Withdraw should return True, 100")
        self.assertEqual(account.withdraw(101), (True, 0), "Withdraw should return True, 0")
        self.assertEqual(account.withdraw(-1), (False, 0), "Withdraw should return False, 0")
        self.assertEqual(account.deposit(-1), (False, 0), "Deposit should return False, 0")
        self.assertEqual(account.balance, 0, "Balance should be 0")
        self.assertEqual(account.credit_balance(), -1, "Credit balance should be -1")


class TestAccountHolder(unittest.TestCase):
    pass


class TestBank(unittest.TestCase):
    pass

    if __name__ == '__main__':
        unittest.main()
