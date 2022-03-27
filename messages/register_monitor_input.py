from __future__ import annotations
from ast import Str
from dataclasses import dataclass
from .marshalable import Marshalable
from  currency_type import CurrencyType
import typing as T

@dataclass 
class RegisterMonitorInput(Marshalable):
    """Class to get input for register monitor service"""
    _name: str
    _account_number: int
    _password: str
    _duration: int

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 3

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        register_monitor_input = RegisterMonitorInput(fields[0], fields[1], fields[2], fields[3])
        return register_monitor_input
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._name,
            1: self._account_number,
            2: self._password,
            3: self._duration,
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
            1: int,
            2: str,
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
    def account_number(self) -> int:
        return self._account_number

    @property
    def duration(self) -> int:
        return self._duration
    
    @duration.setter
    def duration(self, duration: int) -> None:
        self._duration = duration


    def copy(self, other: RegisterMonitorInput) -> None:
        self._name = other._name
        self._account_number = other._account_number
        self._password = other._password
        self._duration = other._duration
