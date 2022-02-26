import pickle
from typing import List

import bcrypt

from BankAccount import BankAccount

database_file = "./bank_accounts.dat"

def saveToBinaryDatabase(bankAccount: BankAccount) -> None:
    bankAccounts = readFromBinaryDatabase()
    bankAccounts.append(bankAccount)
    print(bankAccounts)
    with open(database_file, 'wb') as f:
        for record in bankAccounts:
            print(record)
        pickle.dump(bankAccounts, f)

def readFromBinaryDatabase() -> List[BankAccount]:
    try:
        with open(database_file, 'rb') as f:
            bankAccounts = pickle.load(f)
        print(bankAccounts)
        return bankAccounts
    except: 
        print("File doesn't create; Going to create...")
        return []

def checkIDAndPassword(name: str, accNum: int, password: str) -> BankAccount:
     print("In check pwd")
     bankAccounts = readFromBinaryDatabase()
     for bankAccount in bankAccounts:
         if bankAccount._name == name and bankAccount._accNum == accNum:
             if bcrypt.checkpw(password.encode('utf8'), bankAccount._passwordHash):
                 print("Authorized")
                 return bankAccount
             else:
                 return None
     return None

def getAuthorizationMessage(authorized: bool) -> str:
    if authorized:
        return "Credentials Verified"
    else:
        return "Either account number, name or password is incorrect. Please check again."
 
def updateRecord(editedBankAccount: BankAccount) -> bool:
    print("In update record")
    bankAccounts = readFromBinaryDatabase()
    successStatus = False
    for i, bankAccount in enumerate(bankAccounts):
        if editedBankAccount.equals(bankAccount):
            bankAccounts[i].copy(editedBankAccount)
            successStatus = True
            break
    if not successStatus:
        return False
    with open(database_file, 'wb') as f:
        pickle.dump(bankAccounts, f)
    return True