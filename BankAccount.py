from dataclasses import dataclass
from  CurrencyType import CurrencyType

@dataclass 
class BankAccount:
    """Class for keeping track of bank account information"""
    _name: str
    _accNum: int
    _passwordHash: str
    _currencyType: CurrencyType = 1
    _accBalance: float = 0.0

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def accNum(self) -> int:
        return self._accNum
    
    @name.setter
    def accNum(self, accNum: int) -> None:
        self._accNum = accNum

    @property
    def passwordHash(self) -> str:
        return self._passwordHash

    @property
    def currencyType(self) -> CurrencyType:
        return self._currencyType
    
    @name.setter
    def currencyType(self, currencyType: int) -> None:
        self._currencyType = CurrencyType(currencyType)

    @property
    def accBalance(self) -> float:
        return self._accBalance
    
    @name.setter
    def accBalance(self, accBalance: float) -> None:
        self._accBalance = accBalance
