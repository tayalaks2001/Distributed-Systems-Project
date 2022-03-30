from services import query_balance
from messages.create_new_account_output import CreateNewAccountOutput
from currency_type import CurrencyType
from unmarshaller import decompile_message
import socket
import utils
import random
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

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.settimeout(0.5)

def send_and_recv(obj, port, msg_id):
    bytesToSend = compile_message(msg_id, obj)
    UDPClientSocket.sendto(bytesToSend, ("localhost", port))
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg_id, obj = decompile_message(msgFromServer[0])
    msg = "Message from Server {}".format(obj)
    return obj

test_acc = f"test{random.randint(1,1000000)}" 
password = "1"*11
init_bal = 1000
currency_type = CurrencyType.SGD
obj: CreateNewAccountOutput = send_and_recv(CreateNewAccountInput(test_acc, password, init_bal, currency_type), 2222, 0)
acc_num = obj.account_number

# message sent to lossless server
send_and_recv(BalanceMessage(test_acc, acc_num, password), 2222, 0)

# message sent to lossy server
while True:
    try:
        send_and_recv(WithdrawMessage(test_acc, acc_num, password, CurrencyType.SGD, 1), 5555, 0)
        break
    except socket.timeout:
        continue
        

# message sent to lossless server
print(send_and_recv(BalanceMessage(test_acc, acc_num, password), 2222, 0).balance)

