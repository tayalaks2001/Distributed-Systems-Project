from __future__ import annotations
from dataclasses import dataclass
from .marshalable import Marshalable
from Monitor import Monitor
from  currency_type import CurrencyType
import typing as T

@dataclass 
class RegisterMonitorOutput(Marshalable):
    """Class to produce output for register monitor service"""
    _message: str

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 4

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        register_monitor_output = RegisterMonitorOutput(fields[0])
        return register_monitor_output
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._message
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
        }

    @property
    def message(self) -> float:
        return self._message
    
    @message.setter
    def message(self, message: float) -> None:
        self._message = message

    def copy(self, other: RegisterMonitorOutput) -> None:
        self._message = other._message
