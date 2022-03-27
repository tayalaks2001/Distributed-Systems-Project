from dataclasses import dataclass
from marshalable import Marshalable
import typing as T

@dataclass 
class MonitorResponse(Marshalable):
    """Class to return appropriate error message to client"""
    message: str

    @staticmethod
    def object_type():
        # TODO: Add proper object type
        return 999

    @staticmethod 
    def from_fields(fields: T.Dict[int, T.Any]) -> "Marshalable":
        # TODO: Implement actual construction from fields
        return MonitorResponse(fields[0])
    
    def get_fields(self) -> T.Dict[int, T.Any]:
        # TODO: Implement actual getting of fields
        return {
            0: self.message
        }

    @staticmethod
    def get_field_types() -> T.Dict[int, type]:
        return {
            0: str,
        }

