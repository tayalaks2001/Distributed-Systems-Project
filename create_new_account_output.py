from __future__ import annotations
from dataclasses import dataclass
from marshalable import Marshalable
from  currency_type import CurrencyType
import typing as T

@dataclass 
class CreateNewAccountOutput(Marshalable):
    """Class to produce output for create account service"""
    _account_number: int

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 2

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        create_account_output = CreateNewAccountOutput(fields[0])
        return create_account_output
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._account_number
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: int,
        }

    @property
    def account_number(self) -> str:
        return self._account_number
    
    @account_number.setter
    def account_number(self, account_number: str) -> None:
        self._account_number = account_number

    def copy(self, other: CreateNewAccountOutput) -> None:
        self._account_number = other._account_number
