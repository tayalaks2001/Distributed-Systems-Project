from __future__ import annotations
from dataclasses import dataclass
from marshalable import Marshalable
from monitor import Monitor
from  currency_type import CurrencyType
import typing as T

@dataclass 
class RegisterMonitorOutput(Marshalable):
    """Class to produce output for create account service"""
    _monitor: Monitor
    _update_message: str

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 4

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        register_monitor_output = RegisterMonitorOutput(fields[0], fields[1])
        return register_monitor_output
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._monitor,
            1: self._update_message
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: Monitor,
            1: str,
        }

    @property
    def monitor(self) -> Monitor:
        return self._monitor

    @property
    def update_message(self) -> float:
        return self._update_message
    
    @update_message.setter
    def update_message(self, update_message: float) -> None:
        self._update_message = update_message

    def copy(self, other: RegisterMonitorOutput) -> None:
        self._monitor = other._monitor
        self._update_message = other._update_message
