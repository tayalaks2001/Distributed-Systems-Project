from __future__ import annotations
from dataclasses import dataclass
from marshalable import Marshalable
import typing as T

@dataclass 
class ErrorMessage(Marshalable):
    """Class to return appropriate error message to client"""
    _error_code: int
    _message: str

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 7

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        error_message = ErrorMessage(fields[0], fields[1])
        return error_message
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._error_code,
            1: self._message
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: int,
            1: str,
        }

    @property
    def error_code(self) -> int:
        return self._error_code
    
    @error_code.setter
    def error_code(self, error_code: int) -> None:
        self._error_code = error_code
    
    @property
    def message(self) -> str:
        return self._message
    
    @message.setter
    def message(self, message: str) -> None:
        self._message = message

    def copy(self, other: ErrorMessage) -> None:
        self._error_code = other._error_code
        self._message = other._message
