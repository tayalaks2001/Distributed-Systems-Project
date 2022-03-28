from server import _Server
import time

class SampleServer(_Server):
    def handle(self, msg_id, obj, address):
        return super().handle(msg_id, obj, address)

    def server_loop(self):
        while True:
            msg, address = self.socket.recvfrom(1024)
            print(msg, address)
            # self.socket.sendto(b"Reply to: "+ msg, address)
            # if msg == b"monitor":
            #     for x in range(50):
            #         time.sleep(60/50)
            #         self.socket.sendto(f"{x}".encode(), address)

    

if __name__ == "__main__":
    s = SampleServer("localhost", 50000)
    s.server_loop()
