from enum import Enum

from currency_type import CurrencyType
from .marshalable import Marshalable
from dataclasses import dataclass
import typing as T

@dataclass
class DWBaseMessage(Marshalable):

    name: str
    account_num: int
    password: str
    currency_type: CurrencyType
    amount: float

    def get_fields(self):
        return {
            0: self.name,
            1: self.account_num,
            2: self.password,
            3: self.currency_type,
            4: self.amount,
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
            1: int,
            2: str,
            3: Enum,
            4: float
        }

class DepositMessage(DWBaseMessage):

    @staticmethod
    def from_fields(fields: T.Dict[int, T.Any]):
        return DepositMessage(fields[0], fields[1], fields[2], fields[3], fields[4])

    @staticmethod
    def object_type():
        return 600

class WithdrawMessage(DWBaseMessage):
    @staticmethod
    def from_fields(fields: T.Dict[int, T.Any]):
        return WithdrawMessage(fields[0], fields[1], fields[2], fields[3], fields[4])

    @staticmethod
    def object_type():
        return 601
