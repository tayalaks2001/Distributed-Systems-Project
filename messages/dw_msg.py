from .marshalable import Marshalable
from dataclasses import dataclass
import typing as T

@dataclass
class DWBaseMessage(Marshalable):

    name: str
    account_num: int
    password: str
    currency_type: int
    amount: float

    def get_fields(self):
        return {
            1: self.name,
            2: self.account_num,
            3: self.password,
            4: self.currency_type,
            5: self.amount,
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            1: str,
            2: int,
            3: str,
            4: int,
            5: float
        }

class DepositMessage(DWBaseMessage):

    @staticmethod
    def from_fields(fields: T.Dict[int, T.Any]):
        return DepositMessage(fields[1], fields[2], fields[3], fields[4], fields[5])

    @staticmethod
    def object_type():
        return 600

class WithdrawMessage(DWBaseMessage):
    @staticmethod
    def from_fields(fields: T.Dict[int, T.Any]):
        return WithdrawMessage(fields[1], fields[2], fields[3], fields[4], fields[5])

    @staticmethod
    def object_type():
        return 601
