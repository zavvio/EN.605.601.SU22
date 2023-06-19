import pickle
import threading
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct
from product.Common.userStatus import UserStatus


class ServerCommandReceiver(threading.Thread):
    def __init__(self, logger, network_connection_manager, server_command_issuer):
        threading.Thread.__init__(self)
        self.logger = logger
        self.network_connection_manager = network_connection_manager
        self.server_command_issuer = server_command_issuer
        self.player_status = UserStatus.psIdle
        self.user_id = -1
        self.active_player_id = -1
        self.player_id_1 = -1
        self.player_id_2 = -1
        self.player_id_3 = -1
        self.score1a = -1
        self.score1b = -1
        self.score2a = -1
        self.score2b = -1
        self.score3a = -1
        self.score3b = -1
        self.token1 = -1
        self.token2 = -1
        self.token3 = -1
        self.question = None
        self.question_set1 = None
        self.question_set2 = None
        self.status_packet = ...
        # self.is_spin_ready = ...
        self.chosen_sector = -1
        self.status_msg = 'Awaiting players to join...\n'
        self.question_num = ...
        self.round_num = -1
        self.remaining_spins = -1
        self.answer_result = None
        self.pick_category = -1
        self.show_question_from_picking = False
        self.token_decision = None

    def run(self):
        while True:
            sock = self.network_connection_manager.get_server_socket()
            if sock is None:
                self.logger.error(f'Socket to server does not exist.')
                return -1
            try:
                data = sock.recv(8192)
                if not data:
                    self.logger.error(f'No data.')
                    return -1
                command = pickle.loads(data)
                self.process_command(command)
            except OSError as ose:
                self.logger.debug(f'{ose}')
                return -1

    def process_command(self, command):
        match command.command:
            case Ct.cmdQuestion:
                # print(f'Command [Question] - data type: {type(command.data)}')
                question = command.data
                self.logger.info(f'Command [Question] - Received question: {question.question}')
                self.logger.info(f'Options - A: {question.option_A}, B: {question.option_B}, C: {question.option_C}')
                self.player_status = UserStatus.psShowQuestion
                self.question = question
            case Ct.cmdDeliveryScore:
                score = command.data
                self.logger.info(f'Current score = {score}')
            case Ct.cmdQuestionSet:
                if command.count == 1:
                    self.question_set1 = command.data
                    # for question in self.question_set1.questions:
                    #     print(question.question)
                else:
                    self.question_set2 = command.data
                    # for question in self.question_set2.questions:
                    #     print(question.question)
                self.logger.info(f'Received question set {command.count}')
            case Ct.cmdStatusPacket:
                self.status_packet = command.data
                self.player_status = self.status_packet.status
                self.active_player_id = self.status_packet.active_player_id
                self.status_msg = self.status_packet.status_msg
                self.question_num = self.status_packet.question_num
                self.round_num = self.status_packet.round_num
                self.remaining_spins = self.status_packet.remaining_spins
                self.chosen_sector = self.status_packet.spin_result
                self.player_id_1 = self.status_packet.player_id_1
                self.player_id_2 = self.status_packet.player_id_2
                self.player_id_3 = self.status_packet.player_id_3
                self.score1a = self.status_packet.score1a
                self.score1b = self.status_packet.score1b
                self.score2a = self.status_packet.score2a
                self.score2b = self.status_packet.score2b
                self.score3a = self.status_packet.score3a
                self.score3b = self.status_packet.score3b
                self.token1 = self.status_packet.token1
                self.token2 = self.status_packet.token2
                self.token3 = self.status_packet.token3
                self.answer_result = self.status_packet.answer_result
                self.logger.info(f'Received game status update; player_status = {self.player_status}')
                print(self.status_packet.status_msg)
                print(f'chosen_sector = {self.chosen_sector}')
                if self.active_player_id != self.user_id and "picked category" in self.status_msg:
                    self.show_question_from_picking = True
            case _:
                self.logger.error(f'Undefined command: {command.command}')
                return -1
        return 0
