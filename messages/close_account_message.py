from dataclasses import dataclass
from marshalable import Marshalable
import typing as T

@dataclass 
class CloseAccountMessage(Marshalable):
    """Class to get input for create account service"""
    _name: str
    _account_number: int
    _password: str

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 9

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        delete_account_message = CloseAccountMessage(fields[0], fields[1], fields[2])
        return delete_account_message
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        return {
            0: self._name,
            1: self._account_number,
            2: self._password
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
            1: int,
            2: str
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
    
    @account_number.setter
    def account_number(self, account_number: int) -> None:
        self._account_number = account_number

    def copy(self, other) -> None:
        self._name = other._name
        self._account_number = other._account_number
        self._password = other._password
