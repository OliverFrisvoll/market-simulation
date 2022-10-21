import uuid


class Actor:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.idd = uuid.uuid4()

    def __str__(self):
        return f"{self.name} {self.balance}"

    def __eq__(self, other):
        return self.idd == other.idd
