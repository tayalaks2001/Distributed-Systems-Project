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

    __conversion_tbl__ ={
                            "SGD":{
                                    "INR": 55.83, 
                                    "USD": 0.74
                                    },
                            "USD":{
                                    "SGD": 1.36,
                                    "INR": 75.94

                            }, 
                            "INR":{
                                    "SGD": 0.018,
                                    "USD": 0.013
                            }
                        }

    @staticmethod
    def object_type():
        return 10
    
    

def convert_currency(currency_from: CurrencyType, currency_to: CurrencyType, value: float):

    if currency_from == currency_to:
        return value

    multiplying_factor = CurrencyType.__conversion_tbl__[currency_from.name][currency_to.name]
    
    return value * multiplying_factor