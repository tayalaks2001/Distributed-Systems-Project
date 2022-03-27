from datetime import *
import typing as T

class Monitor:
    def __init__(self, address: T.Tuple[str, int], duration: timedelta):
        self.address = address
        self.expiry = datetime.now() + duration

    def check_expired(self):
        return datetime.now() > self.expiry
