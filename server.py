from marshalable import Marshalable
from monitor_response import MonitorResponse
from Monitor import Monitor
from marshaller import compile_message
import socket
import enum
from unmarshaller import decompile_message
from functools import singledispatchmethod
from collections import defaultdict

import typing as T

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

class ExecutionSemantics(enum.Enum):
    ATLEAST_ONCE = 1
    ATMOST_ONCE = 2

class Server:
    # TODO: Implement appending of created monitors, removal of expired monitors, and sending callback messages

    def __init__(self, addr, port, execution_semantics=ExecutionSemantics.ATLEAST_ONCE) -> None:
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((addr, port))
        self.monitors: T.List[Monitor] = []
        self.execution_semantics = execution_semantics
        if self.execution_semantics == ExecutionSemantics.ATMOST_ONCE:
            self.setup_atmost_once_dict()


    def setup_atmost_once_dict(self):
        self._recvd_dict: T.Dict[T.Tuple[str, int], T.Dict[int, Marshalable]] = defaultdict(dict)

    def server_loop(self):
        while True:
            msg, address = self.socket.recvfrom(1024)
            msg_id, obj = decompile_message(msg)
            try:
                self.handle(msg_id, obj, address)

            except NotImplementedError as e:
                print(e)

    def send(self, msg, addr):
        self.socket.sendto(msg, addr)
        print(f"Sent {msg=} to {addr=}")

    def handle(self, msg_id, obj, address):
        if self.execution_semantics == ExecutionSemantics.ATMOST_ONCE and address in self._recvd_dict and msg_id in self._recvd_dict[address]:
            response = self._recvd_dict[address][msg_id]
            self.send(compile_message(msg_id, response), address)

        else:
            response, update_message = self._handle(obj, address)

            if self.execution_semantics == ExecutionSemantics.ATMOST_ONCE:
                self._recvd_dict[address][msg_id] = response

            self.send(compile_message(msg_id, response), address)
            self._send_update_message(update_message)


    def _send_update_message(self, update_msg):
        print(self.monitors)
        new_monitors = []
        for monitor in self.monitors:
            if not monitor.check_expired():
                new_monitors.append(monitor)
                self.send(compile_message(0, MonitorResponse(update_msg)), monitor.address)
                
        self.monitors = new_monitors

    @singledispatchmethod
    def _handle(self, msg, addr):
        raise NotImplementedError(f"Msg of type {type(msg)} has not been handled")

    @_handle.register
    def _handle_deposit(self, deposit_msg: dw_msg.DepositMessage, addr):
        return services.deposit(deposit_msg.name, deposit_msg.account_num, deposit_msg.password, deposit_msg.currency_type, deposit_msg.amount)

    @_handle.register
    def _handle_withdraw(self, withdraw_msg: dw_msg.WithdrawMessage, addr):
        return services.withdraw(withdraw_msg.name, withdraw_msg.account_num, withdraw_msg.password, withdraw_msg.currency_type, withdraw_msg.amount)
                
    @_handle.register
    def _handle_transfer(self, transfer_msg: transfer_input.TransferInput, addr):
        return services.transfer(transfer_msg.name, transfer_msg.account_number, transfer_msg.password, transfer_msg.currency_type, transfer_msg.transfer_amount, transfer_msg.recipient_account_number)

    @_handle.register
    def _handle_balance(self, balance_msg: balance_msg.BalanceMessage, addr):
        return services.query_balance(balance_msg.name, balance_msg.account_num, balance_msg.password)

    @_handle.register
    def _handle_monitor(self, monitor_msg: register_monitor_input.RegisterMonitorInput, addr):
        response, monitor, update_msg = services.register_monitor(monitor_msg.name, monitor_msg.account_number, monitor_msg.password, monitor_msg.duration, addr)
        self.monitors.append(monitor)
        return response, update_msg

    @_handle.register
    def _handle_new_acc(self, new_acc_msg: create_new_account_input.CreateNewAccountInput, addr):
        return services.create_new_account(new_acc_msg.name, new_acc_msg.password, new_acc_msg.initial_balance, new_acc_msg.currency_type.value)

if __name__ == "__main__":
    s = Server("127.0.0.1", 2222, ExecutionSemantics.ATMOST_ONCE)
    s.server_loop()
