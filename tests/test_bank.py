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
        debt = Debt(100, "loan", 0, actor_id, creditor_id)
        self.assertRaises(ValueError, debt.repay, -1)
        self.assertEqual(debt.repay(101), (True, -1), "Repay should return True, -1")

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
        self.assertEqual(credit.credit(0), (True, 100), "Repay credit should return True, 100")


class TestAccount(unittest.TestCase):

    def test_account_name(self):
        account = Account("name", 100)
        self.assertEqual(account._account_name, "name", "Account name should be name")

    def test_account_id(self):
        account = Account("name", 100)
        account_id = account.account_id
        self.assertEqual(account.account_id, account_id, "Account id should be the same")

    def test_balance_without_credit(self):
        account = Account("name", 100)
        self.assertEqual(account.balance, 100, "Balance should be 100")
        self.assertEqual(account.deposit(50), (True, 150), "Deposit should return True, 150")
        self.assertEqual(account.balance, 150, "Balance should be 150")
        self.assertEqual(account.withdraw(50), (True, 100), "Withdraw should return True, 100")
        self.assertEqual(account.withdraw(101), (False, 100), "Withdraw should return False, 100")
        self.assertEqual(account.withdraw(-1), (False, 100), "Withdraw should return False, 100")
        self.assertEqual(account.deposit(-1), (False, 100), "Deposit should return False, 100")
        self.assertEqual(account.balance, 100, "Balance should be 100")
        self.assertEqual(account.credit_balance(), 0, "Credit balance should be 0")

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
        self.assertEqual(account.credit(-89), (True, 10), "Credit should return True and 10")
        self.assertEqual(account.withdraw(11), (False, 0), "Withdraw should return False, 10")
        self.assertEqual(account.available_credit(), 10, "Available credit should be 10")
        self.assertEqual(account.credit(-10), (True, 0), "Credit should return True and 0")
        self.assertEqual(account.withdraw(1), (False, 0), "Withdraw should return False, 0")


class TestAccountHolder(unittest.TestCase):
    def test_actor_id(self):
        actor_id = uuid.uuid4()
        account_holder = AccountHolder(actor_id)
        self.assertEqual(account_holder.actor_id, actor_id, "Actor id should be the same")

    def test_accounts(self):
        actor_id = uuid.uuid4()
        account_holder = AccountHolder(actor_id)
        account_name = "name"
        status, account_id = account_holder.add_account(account_name, 100)
        self.assertTrue(status, "Add account should return True")
        self.assertEqual(account_holder.get_account(account_id).balance, 100, "Balance should be 100")


class TestBank(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
