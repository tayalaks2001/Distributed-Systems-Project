import abc
from Monitor import Monitor
from marshaller import compile_message
import socket
import random
from unmarshaller import decompile_message
from functools import singledispatchmethod
from collections import defaultdict

import typing as T

from messages.marshalable import Marshalable
from messages.monitor_response import MonitorResponse

import messages.dw_msg as dw_msg
import messages.balance_msg as balance_msg
import messages.transfer_input as transfer_input
import messages.register_monitor_input as register_monitor_input
import messages.create_new_account_input as create_new_account_input
import messages.close_account_message as close_account_message

# To auto register classes
import messages.transfer_output
import messages.register_monitor_output
import messages.create_new_account_output
import messages.close_account_response as close_account_response

import services


class _Server(abc.ABC):

    def __init__(self, addr, port, success_prob=1.0) -> None:
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((addr, port))
        self.monitors: T.List[Monitor] = []
        self.success_prob = success_prob

    def server_loop(self):
        while True:
            msg, address = self.socket.recvfrom(1024)

            if random.random() > self.success_prob:
                print(f"Dropping request...")
                continue

            msg_id, obj = decompile_message(msg)
            print(obj)
            try:
                self.handle(msg_id, obj, address)

            except NotImplementedError as e:
                print(e)

    def send(self, msg, addr):
        print(f"Sent {msg=} to {addr=}")
        if random.random() > self.success_prob:
            print(f"Dropping response...")
            return
        self.socket.sendto(msg, addr)

    @abc.abstractmethod
    def handle(self, msg_id, obj, address):
        pass

    def _send_update_message(self, update_msg):
        print(self.monitors)
        new_monitors = []
        for monitor in self.monitors:
            if not monitor.check_expired():
                new_monitors.append(monitor)
                self.send(
                    compile_message(0, MonitorResponse(update_msg)), monitor.address
                )

        self.monitors = new_monitors

    @singledispatchmethod
    def _handle(self, msg, addr):
        raise NotImplementedError(f"Msg of type {type(msg)} has not been handled")

    @_handle.register
    def _handle_deposit(self, deposit_msg: dw_msg.DepositMessage, addr):
        return services.deposit(
            deposit_msg.name,
            deposit_msg.account_num,
            deposit_msg.password,
            deposit_msg.currency_type,
            deposit_msg.amount,
        )

    @_handle.register
    def _handle_withdraw(self, withdraw_msg: dw_msg.WithdrawMessage, addr):
        return services.withdraw(
            withdraw_msg.name,
            withdraw_msg.account_num,
            withdraw_msg.password,
            withdraw_msg.currency_type,
            withdraw_msg.amount,
        )

    @_handle.register
    def _handle_transfer(self, transfer_msg: transfer_input.TransferInput, addr):
        return services.transfer(
            transfer_msg.name,
            transfer_msg.account_number,
            transfer_msg.password,
            transfer_msg.currency_type,
            transfer_msg.transfer_amount,
            transfer_msg.recipient_account_number,
        )

    @_handle.register
    def _handle_balance(self, balance_msg: balance_msg.BalanceMessage, addr):
        return services.query_balance(
            balance_msg.name, balance_msg.account_num, balance_msg.password
        )

    @_handle.register
    def _handle_monitor(
        self, monitor_msg: register_monitor_input.RegisterMonitorInput, addr
    ):
        response, monitor, update_msg = services.register_monitor(
            monitor_msg.name,
            monitor_msg.account_number,
            monitor_msg.password,
            monitor_msg.duration,
            addr,
        )
        if monitor is not None: self.monitors.append(monitor)
        return response, update_msg

    @_handle.register
    def _handle_new_acc(
        self, new_acc_msg: create_new_account_input.CreateNewAccountInput, addr
    ):
        return services.create_new_account(
            new_acc_msg.name,
            new_acc_msg.password,
            new_acc_msg.initial_balance,
            new_acc_msg.currency_type.value,
        )
    
    @_handle.register
    def _handle_close_acc(self, close_acc_msg: close_account_message.CloseAccountMessage, addr):
        return services.close_account(
            close_acc_msg.name,
            close_acc_msg.account_number,
            close_acc_msg.password,
        )


class AtmostOnceServer(_Server):
    def __init__(self, addr, port, success_prob) -> None:
        super().__init__(addr, port, success_prob=success_prob)
        self._recvd_dict: T.Dict[
            T.Tuple[str, int], T.Dict[int, Marshalable]
        ] = defaultdict(dict)

    def handle(self, msg_id, obj, address):
        if address in self._recvd_dict and msg_id in self._recvd_dict[address]:
            response = self._recvd_dict[address][msg_id]
            self.send(compile_message(msg_id, response), address)
            return

        response, update_message = self._handle(obj, address)
        print(msg_id)
        print(response)
        print(update_message)
        self._recvd_dict[address][msg_id] = response
        self.send(compile_message(msg_id, response), address)
        self._send_update_message(update_message)


class AtleastOnceServer(_Server):
    def handle(self, msg_id, obj, address):
        response, update_message = self._handle(obj, address)
        self.send(compile_message(msg_id, response), address)
        self._send_update_message(update_message)


if __name__ == "__main__":
    s = AtmostOnceServer("127.0.0.1", 2222)
    s.server_loop()
