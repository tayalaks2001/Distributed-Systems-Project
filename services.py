import bcrypt
import random
from datetime import *
from monitor import Monitor
from services_utils import *

from bank_account import BankAccount 


def create_new_account(name: str, password: str, initialBalance: float, currencyType: int = 1) -> int:
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
        mssg = "Successfully deposited! New Balance " + str (bankAccount._accBalance)
    else:
        mssg = "An error has occurred. Please contact the administrator."
    return mssg
    
def withdraw(name: str, accNum: int, password: str, currencyType: int, amount: float) -> str:
    # TODO: add handling of different currency type to which account is created 

    """Withdraw money from an account.

    Keyword arguments:
    name: Name of Account Holder
    accNum: Account Number
    password: Unhashed password of Account Holder
    currencyType: Currency in which amount is to be withdrawn

    Returns: 
    Message specifying updated balance in account OR appropriate error message
    """
    bankAccount = checkIDAndPassword(name=name, accNum=accNum, password=password)
    authorized = bankAccount is not None
    mssg = getAuthorizationMessage(authorized)
    print(mssg)
    if not authorized:
        return mssg
    
    if (bankAccount._accBalance >= amount):
        bankAccount._accBalance -= amount
        successStatus = updateRecord(editedBankAccount=bankAccount)
        if successStatus:
            mssg = "Successfully withdrawn! New Balance " + str (bankAccount._accBalance)
        else:
            mssg = "An error has occurred. Please contact the administrator."
    else:
        mssg = "Insufficient balance in account"
    return mssg

def register_monitor(name: str, accNum: int, password: str, duration: timedelta, clientIPAddress: str) -> Monitor:
    """Register monitor for database updates. A client can choose to monitor updates to the database for a chosen period of time. 

    Keyword arguments:
    name: Name of Account Holder
    accNum: Account Number
    password: Unhashed password of Account Holder
    duration: Duration of time for which client wants to monitor database updates. 

    Returns: 
    Monitor to be kept track of by server
    """
    bankAccount = checkIDAndPassword(name=name, accNum=accNum, password=password)
    authorized = bankAccount is not None
    mssg = getAuthorizationMessage(authorized)
    print(mssg)
    if not authorized:
        return mssg
    
    monitor = Monitor(clientIPAddress, duration)
    return monitor

def query_balance(name: str, accNum: int, password: str) -> float:
    """Query balance in account.

    Keyword arguments:
    name: Name of Account Holder
    accNum: Account Number
    password: Unhashed password of Account Holder

    Returns: 
    Account Balance
    """
    bankAccount = checkIDAndPassword(name=name, accNum=accNum, password=password)
    authorized = bankAccount is not None
    mssg = getAuthorizationMessage(authorized)
    print(mssg)
    if not authorized:
        return mssg

    return bankAccount._accBalance


if __name__ == '__main__':
    # Test create new account
    # accNum = create_new_account("Aks", "password345", 1500.0, 3)
    # print("New account created with account number: " + str(accNum))

    # Test deposit money into account
    # print(deposit("Aru", 36446843756051, "password234", 1, 350))
    # print("Final values")
    # readFromBinaryDatabase()

    # Test withdraw money from account
    # print(withdraw("Aks", 7711473574125, "password345", 1, 1000))
    # print("Final values")
    # readFromBinaryDatabase()

    # Test Query Balance
    # balance = query_balance("Aks", 7711473574125, "password345")
    # print("Balance in account: " + str(balance))
    # print("Final values")
    # readFromBinaryDatabase()

    pass
