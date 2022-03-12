from datetime import *

class Monitor:
    def __init__(self, clientIPAddress: str, duration: timedelta):
        self.clientIPAddress = clientIPAddress
        self.expiry = datetime.now() + duration

    def checkExpiry(self):
        return datetime.now() < self.expiry