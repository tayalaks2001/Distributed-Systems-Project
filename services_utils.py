import pickle

from BankAccount import BankAccount

database_file = "./bank_accounts.dat"

def saveToBinaryDatabase(bankAccount: BankAccount):
    bankAccounts = readFromBinaryDatabase()
    bankAccounts.append(bankAccount)
    print(bankAccounts)
    with open(database_file, 'wb') as f:
        for record in bankAccounts:
            print(record)
        pickle.dump(bankAccounts, f)

def readFromBinaryDatabase():
    try:
        with open(database_file, 'rb') as f:
            bankAccounts = pickle.load(f)
        print(bankAccounts)
        return bankAccounts
    except: 
        print("File doesn't create; Going to create...")
        return []

def checkIfRecordExists():
    # TODO
    pass