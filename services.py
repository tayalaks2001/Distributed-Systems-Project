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

    updateMssg = "New Account Created by " + str(bankAccount._name) + "with Account Number: " + str(accNum)
    # save to binary file
    saveToBinaryDatabase(bankAccount)
    return accNum, updateMssg

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
    
    updateMssg = str(bankAccount._name) + " desposited " + str(amount) + " into their account with Account Number: " + str(accNum)

    return mssg, updateMssg
    
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
    
    updateMssg = str(bankAccount._name) + " withdrew " + str(amount) + " from their account with Account Number: " + str(accNum)

    return mssg, updateMssg

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

    updateMssg = str(bankAccount._name) + " with Account Number: " + str(accNum) + " registered a monitor."

    return monitor, updateMssg

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

    updateMssg = str(bankAccount._name) + " queried the balance in their account with Account Number: " + str(accNum)

    return bankAccount._accBalance, updateMssg

def transfer(name: str, accNum: int, password: str, currencyType: int,transferAmount: float, recipientAccNum: int) -> str:
    """Query balance in account.

    Keyword arguments:
    name: Name of Account Holder
    accNum: Account Number
    password: Unhashed password of Account Holder
    transferAmount: Amount of money to be transferred
    recipientAccNum: Account Number of Recipient

    Returns: 
    Message specifying updated balance in account after transfer OR appropriate error message
    """
    bankAccount = checkIDAndPassword(name=name, accNum=accNum, password=password)
    authorized = bankAccount is not None
    mssg = getAuthorizationMessage(authorized)
    print(mssg)
    if not authorized:
        return mssg

    if (bankAccount._accBalance < transferAmount):
        return "Insufficient Balance in account"

    recipientBankAccount = getBankAccByAccNum(recipientAccNum)
    if recipientBankAccount is None:
        return "Recipient bank account number provided is incorrect."
    
    bankAccount._accBalance -= transferAmount
    recipientBankAccount._accBalance += transferAmount
    successStatus1 = updateRecord(editedBankAccount=bankAccount)
    successStatus2 = updateRecord(editedBankAccount=recipientBankAccount)

    if successStatus1 and successStatus2:
        mssg = "Successfully transferred! New Balance " + str (bankAccount._accBalance)
    else:
        mssg = "An error has occurred. Please contact the administrator."

    updateMssg = str(bankAccount._name) + " transferred " + str(transferAmount) + " from their account with Account Number: " + str(accNum) + " to account number " + str(recipientAccNum)

    return mssg, updateMssg

if __name__ == '__main__':
    # Test create new account
    # accNum, updateMssg = create_new_account("Aru", "password234", 0.0, 2)
    # print("New account created with account number: " + str(accNum))

    # Test deposit money into account
    # mssg, updateMssg = deposit("Sid", 13398636674566, "password123", 1, 500)
    # print(mssg)
    # print("Final values")
    # readFromBinaryDatabase()

    # Test withdraw money from account
    # mssg, updateMssg = withdraw("Aks", 11456231267882, "password345", 1, 1000)
    # print(mssg)
    # print("Final values")
    # readFromBinaryDatabase()

    # Test Query Balance
    # balance, updateMssg = query_balance("Aks", 11456231267882, "password345")
    # print("Balance in account: " + str(balance))
    # print("Final values")
    # readFromBinaryDatabase()

    # Test Transfer
    # mssg, updateMssg = transfer("Aks", 11456231267882, "password345", 1, 500, 13398636674566)
    # print(mssg)
    # print("Final values")
    # readFromBinaryDatabase()
    # print(updateMssg)

    pass
