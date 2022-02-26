import bcrypt
import random
from services_utils import *

from BankAccount import BankAccount 


def createNewAccount(name: str, password: str, initialBalance: float, currencyType: int = 1) -> int:
    """Create a new account and assign account number.

    Keyword arguments:
    name: Name of Account Holder
    password: Unhashed password of Account Holder
    initialBalance: Initial Balance in Account
    currencyType: Currency in which Account is to be opened

    Returns: 
    Account Number assigned to new Account
    """
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

def deposit(name: str, accNum: int, password: str, currencyType: int, amount: float) -> str:
    # TODO: add handling of different currency type to which account is created 

    """Deposit money into an account.

    Keyword arguments:
    name: Name of Account Holder
    accNum: Account Number
    password: Unhashed password of Account Holder
    currencyType: Currency in which amount is to be deposited

    Returns: 
    Message specifying updated balance in account OR appropriate error message
    """
    bankAccount = checkIDAndPassword(name=name, accNum=accNum, password=password)
    authorized = bankAccount is not None
    mssg = getAuthorizationMessage(authorized)
    print(mssg)
    if not authorized:
        return mssg
    bankAccount._accBalance += amount
    successStatus = updateRecord(editedBankAccount=bankAccount)
    if successStatus:
        mssg = "Successfully deposited!"
    else:
        mssg = "An error has occurred. Please contact the administrator."
    return mssg
    

if __name__ == '__main__':
    # Test create new account
    # accNum = createNewAccount("Aks", "password345", 1500.0, 3)
    # print("New account created with account number: " + str(accNum))

    # Test deposit money into account
    deposit("Aru", 78852030461275, "password234", 1, 350)
    print("Final values")
    readFromBinaryDatabase()
