from __future__ import annotations
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
    
    def equals(self, other: BankAccount) -> bool:
        return self._accNum == other._accNum

    def copy(self, other: BankAccount) -> None:
        self._name = other._name
        self._accBalance = other._accBalance
        self._currencyType = other._currencyType
        self._passwordHash = other._passwordHash

