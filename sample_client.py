import socket
import utils
from marshaller import compile_message
from dw_msg import DepositMessage, WithdrawMessage
from balance_msg import BalanceMessage
from transfer_input import TransferInput
from transfer_output import TransferOutput

msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 2222)

bufferSize          = 1024



# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
bytesToSend = compile_message(TransferInput("aru", 1, "al", 1, 1.1, 2))
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

bytesToSend = compile_message(BalanceMessage("aru", 1, "al"))
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

bytesToSend = compile_message(TransferOutput("asd", "asd"))
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# msgFromServer = UDPClientSocket.recvfrom(bufferSize)



# msg = "Message from Server {}".format(msgFromServer[0])

# print(msg)
