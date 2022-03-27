from unmarshaller import decompile_message
import socket
import utils
from marshaller import compile_message
from messages.dw_msg import DepositMessage, WithdrawMessage
from messages.balance_msg import BalanceMessage
from messages.transfer_input import TransferInput
from messages.transfer_output import TransferOutput
from messages.register_monitor_input import RegisterMonitorInput
from messages.register_monitor_output import RegisterMonitorOutput
from messages.monitor_response import MonitorResponse
from messages.create_new_account_input import CreateNewAccountInput
from messages.error_message import ErrorMessage


msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 2222)

bufferSize          = 1024



# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# # Send to server using created UDP socket
# bytesToSend = compile_message(TransferInput("aru", 1, "al", 1, 1.1, 2))
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# bytesToSend = compile_message(BalanceMessage("aru", 1, "al"))
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# bytesToSend = compile_message(TransferOutput("asd", "asd"))
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

# bytesToSend = compile_message(0, CreateNewAccountInput("aru", "123", 1))
# UDPClientSocket.sendto(bytesToSend, serverAddressPort)

def send_and_recv(obj):
    bytesToSend = compile_message(1, obj)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg_id, obj = decompile_message(msgFromServer[0])
    msg = "Message from Server {}".format(obj)
    print(msg)

acc_num = 11078591594286328903
# obj = BalanceMessage("Aru", acc_num, "password234")
# send_and_recv(obj)

obj = WithdrawMessage("Aru", acc_num, "password234", 1, 100)
send_and_recv(obj)
obj = WithdrawMessage("Aru", acc_num, "password234", 1, 100)
send_and_recv(obj)
# obj = RegisterMonitorInput("Aru", acc_num, "password234", 1)
# send_and_recv(obj)
