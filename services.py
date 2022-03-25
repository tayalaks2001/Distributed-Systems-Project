import uuid
import bcrypt
# import random
from datetime import *
from balance_msg import *
from error_message import ErrorMessage
from register_monitor_output import *
from create_new_account_output import *
from monitor import Monitor
from services_utils import *

from bank_account import BankAccount 


def create_new_account(name: str, password: str, initialBalance: float, currencyType: int = 1) -> T.Tuple[T.Union[CreateNewAccountOutput, ErrorMessage], str]:
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
    id = uuid.uuid1()
    accNum = id.int
    # accNum = int(random.random() * 10 ** 14) 
    
    # generate salt and hash password
    salt = bcrypt.gensalt()
    passwordHash = bcrypt.hashpw(password.encode('utf8'), salt)

    # create new bank account object
    bankAccount = BankAccount(_name=name, _accNum=accNum, _passwordHash=passwordHash, _currencyType=CurrencyType(currencyType), _accBalance=initialBalance)

    updateMssg = "New Account Created by " + str(bankAccount.name) + "with Account Number: " + str(accNum)

    # save to binary file
    saveToBinaryDatabase(bankAccount)
    mssg = "Successfully created new account with account number " + str(accNum)

    response = CreateNewAccountOutput(accNum, mssg)

    return response, updateMssg

def deposit(name: str, accNum: int, password: str, currencyType: int, amount: float) -> T.Tuple[T.Union[BalanceResponse, ErrorMessage], str]:
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
        return ErrorMessage(401, mssg), "Attempted unauthorized access"
    bankAccount.accBalance += amount
    successStatus = updateRecord(editedBankAccount=bankAccount)
    if successStatus:
        mssg = "Successfully deposited! New Balance " + str (bankAccount.accBalance)
    else:
        mssg = "An error has occurred. Please contact the administrator."
        return ErrorMessage(500, mssg), "Database error"
    
    updateMssg = str(bankAccount.name) + " desposited " + str(amount) + " into their account with Account Number: " + str(accNum)

    response = BalanceResponse(bankAccount.accBalance, mssg)

    return response, updateMssg
    
def withdraw(name: str, accNum: int, password: str, currencyType: int, amount: float) -> T.Tuple[T.Union[BalanceResponse, ErrorMessage], str]:
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
        return ErrorMessage(401, mssg), "Attempted unauthorized access"
    
    if (bankAccount.accBalance >= amount):
        bankAccount.accBalance -= amount
        successStatus = updateRecord(editedBankAccount=bankAccount)
        if successStatus:
            mssg = "Successfully withdrawn! New Balance " + str (bankAccount.accBalance)
        else:
            mssg = "An error has occurred. Please contact the administrator."
            return ErrorMessage(501, mssg), "Database error"
    else:
        mssg = "Insufficient balance in account"
        return ErrorMessage(400, mssg), "Attempted withdraw without sufficient balance by " + str(bankAccount.name)
    
    updateMssg = str(bankAccount.name) + " withdrew " + str(amount) + " from their account with Account Number: " + str(accNum)

    response = BalanceResponse(bankAccount.accBalance, mssg)

    return response, updateMssg

def register_monitor(name: str, accNum: int, password: str, duration: int, clientIPAddress: str) -> T.Tuple[T.Union[RegisterMonitorOutput, ErrorMessage], Monitor, str]:
    """Register monitor for database updates. A client can choose to monitor updates to the database for a chosen period of time. 

    Keyword arguments:
    name: Name of Account Holder
    accNum: Account Number
    password: Unhashed password of Account Holder
    duration: Duration of time (in minutes) for which client wants to monitor database updates. 

    Returns: 
    Monitor to be kept track of by server
    """
    bankAccount = checkIDAndPassword(name=name, accNum=accNum, password=password)
    authorized = bankAccount is not None
    mssg = getAuthorizationMessage(authorized)
    print(mssg)
    if not authorized:
        return ErrorMessage(401, mssg), None, "Attempted unauthorized access"
    
    monitor = Monitor(clientIPAddress, duration)

    mssg = "Created monitor for " + str(duration) + " minutes."

    updateMssg = str(bankAccount.name) + " with Account Number: " + str(accNum) + " registered a monitor."

    response = RegisterMonitorOutput(mssg)

    return response, monitor, updateMssg

def query_balance(name: str, accNum: int, password: str) -> T.Tuple[T.Union[BalanceResponse, ErrorMessage], str]:
    """Query balance in account.

    Keyword arguments:
    name: Name of Account Holder
    accNum: Account Number
    password: Unhashed password of Account Holder

    Returns: 
    Message specifying balance in account OR appropriate error message
    """
    bankAccount = checkIDAndPassword(name=name, accNum=accNum, password=password)
    authorized = bankAccount is not None
    mssg = getAuthorizationMessage(authorized)
    print(mssg)
    if not authorized:
        return ErrorMessage(401, mssg), "Attempted unauthorized access"

    updateMssg = str(bankAccount.name) + " queried the balance in their account with Account Number: " + str(accNum)

    mssg = "You have " + str(bankAccount.accBalance) + " " + str(bankAccount.currencyType.name) + " in your bank account"

    response = BalanceResponse(bankAccount.accBalance, mssg)

    return response, updateMssg

def transfer(name: str, accNum: int, password: str, currencyType: int,transferAmount: float, recipientAccNum: int) -> T.Union[T.Tuple[BalanceResponse, str], str]:
    """Transfer amount from one account to another.

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
        return ErrorMessage(401, mssg), "Attempted unauthorized access"

    if (bankAccount.accBalance < transferAmount):
        return ErrorMessage(400, "Insufficient Balance in account"), "Attempted transfer without sufficient balance by " + str(bankAccount.name)

    recipientBankAccount = getBankAccByAccNum(recipientAccNum)
    if recipientBankAccount is None:
        return ErrorMessage(400, "Recipient bank account number provided is incorrect."), "Attempted transfer with incorrect recipient account number by " + str(bankAccount.name)
    
    bankAccount.accBalance -= transferAmount
    recipientBankAccount.accBalance += transferAmount
    successStatus1 = updateRecord(editedBankAccount=bankAccount)
    successStatus2 = updateRecord(editedBankAccount=recipientBankAccount)

    if successStatus1 and successStatus2:
        mssg = "Successfully transferred! New Balance " + str (bankAccount.accBalance)
    else:
        mssg = "An error has occurred. Please contact the administrator."
        return ErrorMessage(501, mssg), "Database error"

    response = BalanceResponse(bankAccount.accBalance, mssg)

    updateMssg = str(bankAccount.name) + " transferred " + str(transferAmount) + " from their account with Account Number: " + str(accNum) + " to account number " + str(recipientAccNum)

    return response, updateMssg

if __name__ == '__main__':
    # Test create new account
    # mssg, updateMssg = create_new_account("Aks", "password345", 1500.0, 3)
    # print(mssg)
    # print(updateMssg)

    # Test deposit money into account
    # mssg, updateMssg = deposit("Sid", 88602177778634412252135967242446744647, "password123", 1, 500)
    # print(mssg)
    # print("Final values")
    # readFromBinaryDatabase()
    # print(updateMssg)

    # Test withdraw money from account
    # mssg, updateMssg = withdraw("Sid", 88602177778634412252135967242446744647, "password123", 1, 150)
    # print(mssg)
    # print("Final values")
    # readFromBinaryDatabase()
    # print(updateMssg)

    # c = CurrencyType.INR
    # print(c.name)

    # Test Query Balance
    balance_mssg, updateMssg = query_balance("Aru", 41923115118426430357812247849916738631, "password234")
    print(balance_mssg)
    print("Final values")
    readFromBinaryDatabase()
    print(updateMssg)
    
    # Test Transfer
    # mssg, updateMssg = transfer("Aks", 119359646033703075354830142254573726791, "password345", 1, 500, 41923115118426430357812247849916738631)
    # print(mssg)
    # print("Final values")
    # readFromBinaryDatabase()
    # print(updateMssg)

    pass
