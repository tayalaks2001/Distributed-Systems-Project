import abc
from enum import Enum, EnumMeta
from messages.marshalable import Marshalable
from messages.marshalable import ABCRegistryMeta

class TempMeta(EnumMeta, ABCRegistryMeta):
    pass

class CurrencyType(Enum):

    """Enum to keep track of currency type of an account"""
    SGD = 1
    USD = 2
    INR = 3 

    @staticmethod
    def object_type():
        return 10