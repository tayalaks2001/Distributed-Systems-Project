import socket
from unmarshaller import decompile_message
from functools import singledispatchmethod

import dw_msg
import balance_msg
import transfer_input
import register_monitor_input
import create_new_account_input

# To auto register classes
import transfer_output
import register_monitor_output
import create_new_account_output

import services

class Server:
    # TODO: Implement appending of created monitors, removal of expired monitors, and sending callback messages

    def __init__(self, addr, port) -> None:
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((addr, port))
        self.monitors = []

    def server_loop(self):
        while True:
            msg, address = self.socket.recvfrom(1024)
            obj = decompile_message(msg)
            try:
                self.handle(obj, address)
            except NotImplementedError as e:
                print(e)


    @singledispatchmethod
    def handle(self, msg, addr):
        raise NotImplementedError(f"Msg of type {type(msg)} has not been handled")

    @handle.register
    def _handle_deposit(self, deposit_msg: dw_msg.DepositMessage, addr):
        return services.deposit(deposit_msg.name, deposit_msg.account_num, deposit_msg.password, deposit_msg.currency_type, deposit_msg.amount)

    @handle.register
    def _handle_withdraw(self, withdraw_msg: dw_msg.WithdrawMessage, addr):
        return services.withdraw(withdraw_msg.name, withdraw_msg.account_num, withdraw_msg.password, withdraw_msg.currency_type, withdraw_msg.amount)
                
    @handle.register
    def _handle_transfer(self, transfer_msg: transfer_input.TransferInput, addr):
        return services.transfer(transfer_msg.name, transfer_msg.account_number, transfer_msg.password, transfer_msg.currency_type, transfer_msg.transfer_amount, transfer_msg.recipient_account_number)

    @handle.register
    def _handle_balance(self, balance_msg: balance_msg.BalanceMessage, addr):
        return services.query_balance(balance_msg.name, balance_msg.account_num, balance_msg.password)

    @handle.register
    def _handle_monitor(self, monitor_msg: register_monitor_input.RegisterMonitorInput, addr):
        return services.register_monitor(monitor_msg.name, monitor_msg.account_number, monitor_msg.password, monitor_msg.duration, monitor_msg.client_ip_address)

    @handle.register
    def _handle_new_acc(self, new_acc_msg: create_new_account_input.CreateNewAccountInput, addr):
        return services.create_new_account(new_acc_msg.name, new_acc_msg.password, new_acc_msg.initial_balance, new_acc_msg.currency_type)

if __name__ == "__main__":
    s = Server("127.0.0.1", 2222)
    s.server_loop()
