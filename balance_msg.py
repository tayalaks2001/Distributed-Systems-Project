from marshalable import Marshalable
from dataclasses import dataclass
import typing as T

@dataclass
class BalanceResponse(Marshalable):
    balance: float

    def get_fields(self):
        return {1: self.balance}

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {1: float}
    
    @staticmethod
    def object_type():
        return 610

    @staticmethod
    def from_fields(fields: T.Dict[int, T.Any]):
        return BalanceResponse(fields[1])

@dataclass
class BalanceRequest(Marshalable):

    name: str
    account_num: int
    password: str

    def get_fields(self):
        return {
            1: self.name,
            2: self.account_num,
            3: self.password,
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            1: str,
            2: int,
            3: str
        }

    @staticmethod
    def from_fields(fields: T.Dict[int, T.Any]):
        return BalanceRequest(fields[1], fields[2], fields[3])

    @staticmethod
    def object_type():
        return 602
