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
    def test_available_credit(self):
        credit = Credit(100, 0, 0)
        self.assertEqual(credit.available_credit(), 100, "Available credit should be 100")

    def test_use_credit(self):
        credit = Credit(100, 0, 0)
        self.assertEqual(credit.credit(-50), (True, 50), "Use credit should return True")
        self.assertEqual(credit.credit(-50), (True, 0), "Use credit should return True")
        self.assertEqual(credit.credit(-1), (False, 0), "Use credit should return False")

    def test_repay_credit(self):
        credit = Credit(100, 0, 0)
        credit.credit(-50)
        self.assertEqual(credit.credit(50), (True, 0), "Repay credit should return True")


class TestAccount(unittest.TestCase):
    pass


class TestAccountHolder(unittest.TestCase):
    pass


class TestBank(unittest.TestCase):
    pass

    if __name__ == '__main__':
        unittest.main()
