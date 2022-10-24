import uuid


class Actor:
    def __init__(self, name):
        self.name = name
        self.actor_id = uuid.uuid4()
        self.bank_accounts: dict = {}
        self.assets: dict = {}
        self.debt: dict = {}
        self.bank = None

    def create_bank_account(self, account_name: str, balance: float):
        if self.bank:
            account = self.bank.create_account(self, account_name, balance)
            if account_name not in self.bank_accounts:
                self.bank_accounts[account_name] = account
            else:
                raise ValueError(f"Account name {account_name} already exists")
        else:
            raise ValueError("Actor has no bank")

    def bank_account(self, account_name: str):
        return self.bank_accounts.get(account_name, None)



    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.actor_id == other.actor_id
