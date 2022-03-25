from datetime import *
import typing as T

class Monitor:
    def __init__(self, address: T.Tuple[str, int], duration: timedelta):
        self.address = address
        self.expiry = datetime.now() + duration

    def checkExpiry(self):
        return datetime.now() < self.expiry