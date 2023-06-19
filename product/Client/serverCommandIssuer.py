import pickle
import socketserver
import time
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct


class ServerCommandIssuer:
    def __init__(self, logger, network_connection_manager):
        self.logger = logger
        self.network_connection_manager = network_connection_manager

    def send_command(self, command):
        sock = self.network_connection_manager.get_server_socket()
        if sock is None:
            self.logger.error(f'Socket to server does not exist.')
            return -1
        try:
            data_string = pickle.dumps(command)
            sock.sendall(data_string)
        except OSError as ose:
            self.logger.error(f'{ose}')
            return -1
        return 0

    def spam_server(self):
        timestamp = 0
        user_id = self.network_connection_manager.get_user_id()
        while True:
            # self.logger.debug(f'Timestamp = {timestamp}')
            command = Command(Ct.cmdKeepAlive, user_id, timestamp)
            timestamp += 1
            if self.send_command(command) < 0:
                break
            if timestamp % 5 == 0:  # Retrieving score every 15 seconds
                self.logger.debug(f'Requesting score from server...')
                time.sleep(1)
                command = Command(Ct.cmdRequestScore, user_id, timestamp)
                if self.send_command(command) < 0:
                    break
            time.sleep(3)
