import pickle
import socketserver
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct


class ClientCommandIssuer:
    def __init__(self, logger, user_manager):
        self.logger = logger
        self.user_manager = user_manager

    def send_command(self, user_id, command):
        user = self.user_manager.get_user(user_id)
        if user is None:
            self.logger.error(f'User {user_id} does not exist.')
            return -1
        sock = user.get_socket()
        if sock is None:
            self.logger.debug(f'Socket for {user_id} does not exist.')
            return -1
        try:
            data_string = pickle.dumps(command)
            sock.sendall(data_string)
        except OSError as ose:
            self.logger.error(f'{ose}')
            return -1
        return 0
