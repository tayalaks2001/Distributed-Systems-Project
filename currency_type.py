from enum import Enum
from messages.marshalable import Marshalable

class CurrencyType(Enum, Marshalable):
    """Enum to keep track of currency type of an account"""
    SGD = 1
    USD = 2
    INR = 3 

    @staticmethod
    def object_type():
        return 10