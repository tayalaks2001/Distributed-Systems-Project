from .marshalable import Marshalable
from dataclasses import dataclass
import typing as T

@dataclass
class BalanceResponse(Marshalable):
    balance: float
    msg: str

    def get_fields(self):
        return {
            0: self.balance,
            1: self.msg
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: float,
            1: str
        }
    
    @staticmethod
    def object_type():
        return 610

    @staticmethod
    def from_fields(fields: T.Dict[int, T.Any]):
        return BalanceResponse(fields[0], fields[1])

@dataclass
class BalanceMessage(Marshalable):

    name: str
    account_num: int
    password: str

    def get_fields(self):
        return {
            0: self.name,
            1: self.account_num,
            2: self.password,
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
            1: int,
            2: str
        }

    @staticmethod
    def from_fields(fields: T.Dict[int, T.Any]):
        return BalanceMessage(fields[0], fields[1], fields[2])

    @staticmethod
    def object_type():
        return 602
