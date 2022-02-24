import bcrypt
import random
from services_utils import *

from BankAccount import BankAccount 

"""Create a new account and assign account number.

Keyword arguments:
Name: Name of Account Holder
Password: Unhashed password of Account Holder
initialBalance: Initial Blaance in Account
currencyType: Currency in which Account is to be opened

Returns: 
Account Number assigned to new Account
"""
def createNewAccount(name: str, password: str, initialBalance: float, currencyType: int = 1) -> int:
    
    # generate 14-digit account number
    accNum = int(random.random() * 10 ** 14) 
    
    # generate salt and hash password
    salt = bcrypt.gensalt()
    passwordHash = bcrypt.hashpw(password.encode('utf8'), salt)

    # create new bank account object
    bankAccount = BankAccount(_name=name, _accNum=accNum, _passwordHash=passwordHash, _currencyType=currencyType, _accBalance=initialBalance)

    # save to binary file
    saveToBinaryDatabase(bankAccount)
    return accNum

if __name__ == '__main__':
    accNum = createNewAccount("Aks", "password345", 1500.0, 3)
    print("New account created with account number: " + str(accNum))
