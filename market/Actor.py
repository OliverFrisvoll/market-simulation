import uuid


class Actor:
    def __init__(self, name, balance):
        self.name = name
        self.actor_id = uuid.uuid4()

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        return self.actor_id == other.actor_id
