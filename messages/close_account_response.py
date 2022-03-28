from __future__ import annotations
from dataclasses import dataclass
from .marshalable import Marshalable
import typing as T

@dataclass 
class CloseAccountResponse(Marshalable):
    """Class to return delete account response message to client"""
    _account_number: int
    _message: str

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 8

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        delete_account_response = CloseAccountResponse(fields[0], fields[1])
        return delete_account_response
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        return {
            0: self._account_number,
            1: self._message
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: int,
            1: str,
        }

    @property
    def account_number(self) -> int:
        return self._account_number
    
    @account_number.setter
    def account_number(self, account_number: int) -> None:
        self._account_number = account_number
    
    @property
    def message(self) -> str:
        return self._message
    
    @message.setter
    def message(self, message: str) -> None:
        self._message = message

    def copy(self, other: CloseAccountResponse) -> None:
        self._account_number = other._account_number
        self._message = other._message
