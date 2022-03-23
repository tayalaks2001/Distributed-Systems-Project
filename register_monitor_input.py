from __future__ import annotations
from ast import Str
from dataclasses import dataclass
from datetime import timedelta
from marshalable import Marshalable
from  currency_type import CurrencyType
import typing as T

@dataclass 
class RegisterMonitorInput(Marshalable):
    """Class to get input for create account service"""
    _name: str
    _account_number: int
    _password: str
    _duration: timedelta
    _client_ip_address: str

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 3

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        register_monitor_input = RegisterMonitorInput(fields[0], fields[1], fields[2], fields[3], fields[4])
        return register_monitor_input
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self._name,
            1: self._account_number,
            2: self._password,
            3: self._duration,
            4: self._client_ip_address,
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
            1: int,
            2: str,
            3: timedelta,
            4: str,
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
    def duration(self) -> timedelta:
        return self._duration
    
    @duration.setter
    def duration(self, duration: timedelta) -> None:
        self._duration = duration

    @property
    def client_ip_address(self) -> str:
        return self._client_ip_address
    
    @name.setter
    def client_ip_address(self, client_ip_address: str) -> None:
        self._client_ip_address = client_ip_address

    def copy(self, other: RegisterMonitorInput) -> None:
        self._name = other._name
        self._account_number = other._account_number
        self._password = other._password
        self._duration = other._duration
        self._client_ip_address = other._client_ip_address
