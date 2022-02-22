import socket
import struct

def send_msg(sock: socket.socket, to_addr, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendto(msg, to_addr)

def recv_msg(sock: socket.socket):
    # Read message length and unpack it into an integer
    raw_msglen, ret_addr = sock.recvfrom(4, socket.MSG_PEEK)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    print(f"{msglen=}")
    return sock.recv(msglen+4)[4:], ret_addr
