from __future__ import annotations
from dataclasses import dataclass
from .marshalable import Marshalable
from currency_type import CurrencyType
import typing as T

@dataclass 
class CreateNewAccountInput(Marshalable):
    """Class to get input for create account service"""
    _name: str
    _password: str
    _initial_balance: float = 0.0
    _currency_type: CurrencyType = 1

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 1

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        create_account_input = CreateNewAccountInput(fields[0], fields[1], fields[2], CurrencyType(fields[3]))
        return create_account_input
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._name,
            1: self._password,
            2: self._initial_balance,
            3: self._currency_type,
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
            1: str,
            2: float,
            3: int,
        }

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def password(self) -> str:
        return self._password

    @property
    def currency_type(self) -> CurrencyType:
        return self._currency_type
    
    @currency_type.setter
    def currency_type(self, currency_type: int) -> None:
        self._currency_type = CurrencyType(currency_type)

    @property
    def initial_balance(self) -> float:
        return self._initial_balance
    
    @initial_balance.setter
    def initial_balance(self, initial_balance: float) -> None:
        self._initial_balance = initial_balance

    def copy(self, other: CreateNewAccountInput) -> None:
        self._name = other._name
        self._initial_balance = other._initial_balance
        self._currency_type = other._currency_type
        self._password = other._password
