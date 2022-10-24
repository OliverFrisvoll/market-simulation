import uuid
from bank import PrivateBank
from actor import Actor

user = Actor("Oliver")

bank = PrivateBank("DNB")

user.bank = bank

user.create_bank_account("Savings", 1000)

user.bank_account("Savings").deposit(1000)

print(user.bank_account("Savings").balance)

