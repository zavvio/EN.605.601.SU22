import pickle
import socket
import threading
import time
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class NetworkConnectionManager:
    def __init__(self, ip_addr='127.0.0.1', port=13579, user_id=1337):
        self.ip_addr = ip_addr
        self.port = port
        self.sock = socket.socket()
        self.user_id = user_id
        self.connect_to_server()

    def connect_to_server(self):
        print(f'Connecting to {self.ip_addr}')
        try:
            self.sock.connect((self.ip_addr, self.port))
            data_string = pickle.dumps(Command(Ct.cmdInit, self.user_id, 0))
            self.sock.sendall(data_string)
            time.sleep(1)
        except OSError as ose:
            print(f'Socket error: {ose}')

    def disconnect_to_server(self):
        self.sock.close()

    def get_server_socket(self):
        return self.sock

    def get_user_id(self):
        return self.user_id
