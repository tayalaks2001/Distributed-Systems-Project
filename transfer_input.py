from __future__ import annotations
from ast import Str
from dataclasses import dataclass
from datetime import timedelta
from marshalable import Marshalable
from  currency_type import CurrencyType
import typing as T

@dataclass 
class TransferInput(Marshalable):
    """Class to get input for create account service"""
    _name: str
    _account_number: int
    _password: str
    _currency_type: int
    _transfer_amount: float
    _recipient_account_number: int

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 5

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        register_monitor_input = TransferInput(fields[0], fields[1], fields[2], fields[3], fields[4], fields[5])
        return register_monitor_input
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._name,
            1: self._account_number,
            2: self._password,
            3: self._currency_type,
            4: self._transfer_amount,
            5: self._recipient_account_number
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
            1: int,
            2: str,
            3: int,
            4: float,
            5: int,
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
    def account_number(self) -> str:
        return self._account_number

    @property
    def currency_type(self) -> int:
        return self._currency_type
    
    @currency_type.setter
    def currency_type(self, currency_type: int) -> None:
        self._currency_type = currency_type

    @property
    def transfer_amount(self) -> float:
        return self._transfer_amount
    
    @transfer_amount.setter
    def transfer_amount(self, transfer_amount: float) -> None:
        self._transfer_amount = transfer_amount
    
    @property
    def recipient_account_number(self) -> int:
        return self._recipient_account_number
    
    @recipient_account_number.setter
    def recipient_account_number(self, recipient_account_number: int) -> None:
        self._recipient_account_number = recipient_account_number

    def copy(self, other: TransferInput) -> None:
        self._name = other._name
        self._account_number = other._account_number
        self._password = other._password
        self._currency_type = other._currency_type
        self._transfer_amount = other._transfer_amount
        self._recipient_account_number = other._recipient_account_number
