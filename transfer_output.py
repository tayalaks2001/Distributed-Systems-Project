from __future__ import annotations
from dataclasses import dataclass
from marshalable import Marshalable
from  currency_type import CurrencyType
import typing as T

@dataclass 
class TransferOutput(Marshalable):
    """Class to produce output for create account service"""
    _message: str
    _update_message: str

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 6

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        transfer_output = TransferOutput(fields[0], fields[1])
        return transfer_output
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._message,
            1: self._update_message
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
            1: str,
        }

    @property
    def message(self) -> str:
        return self._message
    
    @message.setter
    def message(self, message: str) -> str:
        self._message = message

    @property
    def update_message(self) -> float:
        return self._update_message
    
    @update_message.setter
    def update_message(self, update_message: float) -> None:
        self._update_message = update_message

    def copy(self, other: TransferOutput) -> None:
        self._message = other._message
        self._update_message = other._update_message
