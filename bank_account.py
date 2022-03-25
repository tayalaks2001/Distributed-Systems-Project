from __future__ import annotations
from dataclasses import dataclass
from marshalable import Marshalable
from  currency_type import CurrencyType
import typing as T

@dataclass 
class BankAccount(Marshalable):
    """Class for keeping track of bank account information"""
    _name: str
    _accNum: int
    _passwordHash: str
    _currencyType: CurrencyType = CurrencyType.SGD
    _accBalance: float = 0.0

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 0

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        bankAccount = BankAccount(fields[0], fields[1], fields[2], CurrencyType(fields[3]), fields[4])
        return bankAccount
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._name,
            1: self._accNum,
            2: self._passwordHash,
            3: self._currencyType,
            4: self._accBalance,
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
            1: int,
            2: str,
            3: int,
            4: float,
        }

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
    
    @currencyType.setter
    def currencyType(self, currencyType: int) -> None:
        self._currencyType = CurrencyType(currencyType)

    @property
    def accBalance(self) -> float:
        return self._accBalance
    
    @accBalance.setter
    def accBalance(self, accBalance: float) -> None:
        self._accBalance = accBalance
    
    def equals(self, other: BankAccount) -> bool:
        return self._accNum == other._accNum

    def copy(self, other: BankAccount) -> None:
        self._name = other._name
        self._accBalance = other._accBalance
        self._currencyType = other._currencyType
        self._passwordHash = other._passwordHash

