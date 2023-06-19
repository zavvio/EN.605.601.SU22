import pickle
import socketserver
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct
from product.Common.userStatus import UserStatus


class ClientCommandReceiver(socketserver.BaseRequestHandler):
    def handle(self):
        user_id = -1
        while True:
            try:
                data = self.request.recv(4096)
                if not data:
                    break
                command = pickle.loads(data)
                ret = self.process_command(user_id, command)
                if ret > 0:
                    user_id = ret
            # except ConnectionResetError:
            except OSError as ose:
                self.server.logger.debug(f'Connection for user {user_id} was reset. {ose}')
                if user_id > 0:
                    user = self.server.user_manager.get_user(user_id)
                    user.set_socket(None)
                break

    def process_command(self, user_id, command):
        match command.command:
            case Ct.cmdInit:
                # print(f'Command [Init] - data type: {type(command.data)}')
                user_id = command.data
                self.server.user_manager.add_user(user_id)
                user = self.server.user_manager.get_user(user_id)
                user.set_socket(self.request)
                self.server.logger.info(f'Command [Init] - User ID: {user_id}')
                return user_id
            case Ct.cmdReady:
                user_id = command.data
                user = self.server.user_manager.get_user(user_id)
                user.set_status(UserStatus.usReady)
            case Ct.cmdKeepAlive:
                # print(f'Command [KeepAlive] - data type: {type(command.data)}')
                self.server.logger.info(f'Command [KeepAlive] - User ID: {command.data}')
            case Ct.cmdAnswer:
                # status = self.server.user_manager.get_user(user_id)
                # print(f'Received answer {command.data} from {user_id}')
                user = self.server.user_manager.get_user(user_id)
                user.set_status(UserStatus.usAnswer)
                user.set_answer(command.data)
                self.server.logger.info(f'Command [Answer] - {user_id} chose option {command.data}')
            case Ct.cmdRequestScore:
                if user_id != -1:
                    self.server.logger.info(f'Command [RequestScore] - delivering score to user {user_id}')
                    score = self.server.user_manager.get_user(user_id).get_score()
                    cmd = Command(Ct.cmdDeliveryScore, score, 0)
                    if self.server.client_command_issuer.send_command(user_id, cmd) < 0:
                        return -1
            case Ct.cmdSpinWheel:
                user = self.server.user_manager.get_user(user_id)
                user.set_status(UserStatus.usSpin)
                self.server.logger.info(f'Command [SpinWheel] - {user_id} requested to spin wheel')
            case Ct.cmdPickCategory:
                user = self.server.user_manager.get_user(user_id)
                user.set_status(UserStatus.usPickCategory)
                user.category = command.data
                self.server.logger.info(f'Command [PickCategory] - {user_id} picked category {user.category}')
            case Ct.cmdUseToken:
                user = self.server.user_manager.get_user(user_id)
                user.set_status(UserStatus.usUseToken)
                user.use_token = command.data
                if user.use_token is True:
                    self.server.logger.info(f'Command [UseToken] - {user_id} uses token.')
                elif user.use_token is False:
                    self.server.logger.info(f'Command [UseToken] - {user_id} not using token.')
            case _:
                self.server.logger.error(f'Undefined command: {command.command}')
                return -1
        # self.server.logger.info(f'Received command: {command.command}, data: {command.data}, count: {command.count}')
        return 0
