import logging
import socket
import socketserver
import threading
from product.Server.userManager import UserManager
import time


class NetworkConnectionManager(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


# class __NetworkConnectionManager(threading.Thread):
#     def __init__(self, ip_addr='127.0.0.1', port=13579):
#         threading.Thread.__init__(self)
#         self.visitor_count = 0
#         self.sock = socket.socket()
#         self.sock.bind((ip_addr, port))
#         self.sock.listen()
#         print(f'Server initialized.')
#
#     def run(self):
#         while True:
#             client, client_ip_addr = self.sock.accept()
#             self.visitor_count += 1
#             print(f'New client connection from {client_ip_addr}')
#             logging.info(f'New client connection from {client_ip_addr}')
#             command = pickle.loads(client.recv(4096))
#             print(f'Received command: {command.command}, data: {command.data}')
#             client.send(f'You have connected to the GG server, {command.data}.'.encode())
#             client.close()


# class UserManager(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#         while True:
#             time.sleep(1)
#             print(f'Server responsive: {time.ctime(time.time())}')
