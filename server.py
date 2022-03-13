import socket
import utils

class Server:
    def __init__(self, addr, port) -> None:
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((addr, port))
        self.monitors = []

    def server_loop(self):
        while True:
            msg = self.socket.recvfrom(1024)
            print(msg)

if __name__ == "__main__":
    s = Server("127.0.0.1", 2222)
    s.server_loop()