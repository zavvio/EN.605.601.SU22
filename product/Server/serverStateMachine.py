# from multiprocessing.connection import wait
import random
import threading
import time
from datetime import datetime
from enum import Enum
from statemachine import StateMachine, State

from product.Common.command import Command
from product.Common.commandType import CommandType as Ct
from product.Common.statusPacket import StatusPacket
# from product.Server import userStatus
from product.Server.scoreboard import Scoreboard
from product.Common.userStatus import UserStatus
from product.Server.wheel import Wheel


class ServerStateTransition(Enum):
    launch = 1
    send_question_set = 2
    change_active_player = 3
    sync_status = 4
    game_over = 5
    back_to_lobby = 6
    await_response = 7
    spin_wheel = 8
    answer = 9
    pick_category = 10
    sector_category = 11
    sector_spin_to_sync = 12
    sector_change_player = 13
    show_question = 14
    answer_correct = 15
    answer_incorrect = 16
    # check_token = 17
    use_token = 18
    not_use_token = 19


hardcode_player_1 = 1337
hardcode_player_2 = 1234
hardcode_player_3 = 1001


class ServerStateMachine(StateMachine):
    state_start = State('Start State Machine', initial=True)
    state_fill_lobby = State('Waiting for Players')
    state_init = State('Initialize')
    state_send_question_set = State('Send Question Set')
    state_change_active_player = State('Change Active Player')
    state_sync_status = State('Sync Status')
    state_game_over = State('Game Over')
    state_await_player_response = State('Await Player Response')
    state_spin_wheel = State('Spin the Wheel')
    state_sector_category = State('Sector: Category')
    state_answer = State('Answer')
    # state_check_token = State('Check Token')
    # round_init = State('Initializing round')
    # turn_init = State('Initializing turn')
    # waiting_for_turn_player = State('Waiting for current turn player input')
    # finalizing_turn = State('Ending turn')
    # finalizing_round = State('Getting round results')

    start = state_start.to(state_fill_lobby)
    launch = state_fill_lobby.to(state_init)
    send_question_set = state_init.to(state_send_question_set)
    change_active_player = state_send_question_set.to(state_change_active_player)
    sync_status = state_change_active_player.to(state_sync_status)
    game_over = state_sync_status.to(state_game_over)
    back_to_lobby = state_game_over.to(state_fill_lobby)
    await_response = state_sync_status.to(state_await_player_response)
    spin_wheel = state_await_player_response.to(state_spin_wheel)
    answer = state_await_player_response.to(state_answer)
    pick_category = state_await_player_response.to(state_sync_status)
    sector_category = state_spin_wheel.to(state_sector_category)
    sector_spin_to_sync = state_spin_wheel.to(state_sync_status)
    sector_change_player = state_spin_wheel.to(state_change_active_player)
    show_question = state_sector_category.to(state_sync_status)
    answer_correct = state_answer.to(state_sync_status)
    answer_incorrect = state_answer.to(state_sync_status)  # TODO: duplicated transition
    # check_token = state_sync_status.to(state_check_token)
    use_token = state_await_player_response.to(state_sync_status)
    not_use_token = state_await_player_response.to(state_change_active_player)
    # start_round = round_init.to(turn_init)
    # start_turn = turn_init.to(waiting_for_turn_player)
    # end_turn = waiting_for_turn_player.to(finalizing_turn)
    # next_turn = finalizing_turn.to(turn_init)
    # end_round = finalizing_turn.to(finalizing_round)
    # reset = finalizing_round.to(round_init)
    # end_game = finalizing_round.to(game_over)

    def __init__(self, user_manager, client_command_issuer, question_manager):
        super(ServerStateMachine, self).__init__()
        self._lock = threading.Lock()
        self.curr_state = ...
        self.next_state = ...
        # print('__init__')
        self.user_manager = user_manager
        self.client_command_issuer = client_command_issuer
        self.question_manager = question_manager
        self.active_player_index = -1
        self.round_counter = 1
        self.CONST_SPIN_COUNTER = 50
        self.spin_counter = 50
        self.players = ...
        self.question = ...
        self.question_set1 = ...
        self.question_set2 = ...
        self.scoreboard = ...
        self.wheel = ...
        self.game_action = ...
        self.spin_result = ...
        self.answer_result = None
        self.token_result = None
        self.player_awaiting_opponent = None
        # thread_server_state_machine = threading.Thread(target=self.daemon_server_state_machine)  # , daemon=True)
        # thread_server_state_machine.start()

    def daemon_server_state_machine(self):
        self.start()
        while True:
            # time.sleep(1)
            # print(f'daemon_server_state_machine')
            if self.curr_state == self.next_state:
                # print(f'{self.curr_state} == {self.next_state}')
                continue
            with self._lock:
                self.curr_state = self.next_state
                # print(f'{self.curr_state} <-- {self.next_state}')
            match self.curr_state:
                case ServerStateTransition.launch:
                    self.launch()
                case ServerStateTransition.send_question_set:
                    self.send_question_set()
                case ServerStateTransition.change_active_player:
                    self.change_active_player()
                case ServerStateTransition.sync_status:
                    self.sync_status()
                case ServerStateTransition.game_over:
                    self.game_over()
                case ServerStateTransition.back_to_lobby:
                    self.back_to_lobby()
                case ServerStateTransition.await_response:
                    self.await_response()
                case ServerStateTransition.spin_wheel:
                    self.spin_wheel()
                case ServerStateTransition.answer:
                    self.answer()
                case ServerStateTransition.pick_category:
                    self.pick_category()
                case ServerStateTransition.sector_category:
                    self.sector_category()
                case ServerStateTransition.sector_spin_to_sync:
                    self.sector_spin_to_sync()
                case ServerStateTransition.sector_change_player:
                    self.sector_change_player()
                case ServerStateTransition.show_question:
                    self.show_question()
                case ServerStateTransition.answer_correct:
                    self.answer_correct()
                case ServerStateTransition.answer_incorrect:
                    self.answer_incorrect()
                # case ServerStateTransition.check_token:
                #     self.check_token()
                case ServerStateTransition.use_token:
                    self.use_token()
                case ServerStateTransition.not_use_token:
                    self.not_use_token()
                case _:
                    print(f'[ERROR] Unsupported state transtion')

    def on_enter_state_fill_lobby(self):
        # print('Filling lobby')
        print(self.current_state)
        is_lobby_filled = False

        print('Awaiting players...')
        while not is_lobby_filled:
            time.sleep(0.1)
            player1 = self.user_manager.get_user(hardcode_player_1)
            player2 = self.user_manager.get_user(hardcode_player_2)
            # player3 = self.user_manager.get_user(hardcode_player_3)
            if player1 is None or player1.get_socket() is None:
                # print('Player 1 not yet connected.')
                continue
            if player2 is None or player2.get_socket() is None:
                # print('Player 2 not yet connected.')
                continue
            # if player3 is None or player3.get_socket() is None:
            #     print('Player 3 not yet connected.')
            #     continue
            if player1.get_status() != UserStatus.usReady:
                # print('Player 1 not ready.')
                continue
            if player2.get_status() != UserStatus.usReady:
                # print('Player 2 not ready.')
                continue
            # if player3.get_status() != UserStatus.usReady:
            #     print('Player 3 not ready.')
            #     continue
            is_lobby_filled = True

        # self.launch()
        with self._lock:
            self.next_state = ServerStateTransition.launch

    def on_enter_state_init(self):
        # print('Initializing')
        print('All players ready...')
        print(self.current_state)

        self.round_counter = 1
        self.spin_counter = self.CONST_SPIN_COUNTER
        self.game_action = UserStatus.gaSpin
        player1 = self.user_manager.get_user(hardcode_player_1)
        player2 = self.user_manager.get_user(hardcode_player_2)
        player3 = self.user_manager.get_user(hardcode_player_3)
        player1.clear_game_stat()
        player2.clear_game_stat()
        player3.clear_game_stat()
        self.players = [player1, player2, player3]
        self.active_player_index = random.randint(0, len(self.players)-1)
        self.scoreboard = Scoreboard(self.user_manager, self.players)
        self.question_set1, self.question_set2 = self.question_manager.get_random_question_set()
        self.wheel = Wheel(self.question_set1.get_list_of_categories())
        print(f'Starting game with {len(self.players)} players')

        # self.send_question_set()
        with self._lock:
            self.next_state = ServerStateTransition.send_question_set
            print(f'self.next_state = {self.next_state}')

    def on_enter_state_send_question_set(self):
        print(self.current_state)
        command1 = Command(Ct.cmdQuestionSet, self.question_set1, 1)
        command2 = Command(Ct.cmdQuestionSet, self.question_set2, 2)
        for p in self.players:
            self.client_command_issuer.send_command(p.get_user_id(), command1)
            time.sleep(0.5)
            self.client_command_issuer.send_command(p.get_user_id(), command2)
            time.sleep(0.5)
        # self.change_active_player()
        with self._lock:
            self.next_state = ServerStateTransition.change_active_player

    def on_enter_state_change_active_player(self):
        print(self.current_state)
        self.active_player_index = (self.active_player_index + 1) % len(self.players)
        # self.sync_status()
        with self._lock:
            self.next_state = ServerStateTransition.sync_status

    def on_enter_state_sync_status(self):
        print(self.current_state)
        status_message = ''
        if self.player_awaiting_opponent is not None:
            self.active_player_index = (self.active_player_index + len(self.players) - 1) % len(self.players)
        active_player = self.players[self.active_player_index]
        active_player.set_status(UserStatus.usIdle)
        non_active_players = [p for p in self.players if p != active_player]
        for p in non_active_players:
            p.set_status(UserStatus.usIdle)

        status_inactive = UserStatus.psWait
        status_active = status_inactive
        question_set = self.question_set1
        if self.round_counter == 1:
            question_set = self.question_set1
        elif self.round_counter == 2:
            question_set = self.question_set2
        match self.game_action:
            case UserStatus.gaSpin:
                status_active = UserStatus.psSpin
                status_message = f'Player {active_player.get_user_id()} can spin.'
                if self.answer_result is not None:
                    status_message = f'The answer is {self.question.answer}. {status_message}'
                    if self.answer_result:
                        status_message = f'Correct, {status_message}'
                    else:  # TODO: dead-code, shouldn't arrive here
                        status_message = f'Incorrect, {status_message}'
                if self.token_result is True:
                    status_message = f'Token used, {status_message}'
                elif self.token_result is False:
                    status_message = f'Token not used, {status_message}'
            case UserStatus.gaAnswer:
                status_active = UserStatus.psShowQuestion
                if self.player_awaiting_opponent is None and active_player.category == -1:
                    status_message = f'Player {active_player.get_user_id()} landed on ' \
                                     f'{question_set.categories[self.spin_result % 9]}, showing question~'
                elif self.player_awaiting_opponent is None and active_player.category != -1:
                    self.spin_result = active_player.category
                    status_message = f'Player {active_player.get_user_id()} picked ' \
                                     f'category {question_set.categories[self.spin_result % 9]}, showing question~'
                elif self.player_awaiting_opponent is not None:
                    self.player_awaiting_opponent = None
                    opponent = self.players[(self.active_player_index + 1) % len(self.players)]
                    self.spin_result = opponent.category
                    status_message = f'Player {opponent.get_user_id()} picked ' \
                                     f'category {question_set.categories[self.spin_result % 9]} ' \
                                     f'for Player {active_player.get_user_id()}, showing question~'
                else:
                    # TODO: shouldn't be here
                    print(f'[ERROR] Shouldn\'t be here!')
            case UserStatus.gaCategoryCompleted:
                status_active = UserStatus.psSpin
                status_message = f'Player {active_player.get_user_id()} landed on' \
                                 f' {question_set.categories[self.spin_result % 9]} [completed], spin again.'
            case UserStatus.gaSpinAgain:
                status_active = UserStatus.psSpinAgain
                status_message = f'Player {active_player.get_user_id()} landed on Spin Again, do it.'
            case UserStatus.gaBankrupt:
                status_active = UserStatus.psSpin
                previous_player = self.players[(self.active_player_index + len(self.players) - 1) % len(self.players)]
                status_message = f'Player {previous_player.get_user_id()} gone bankrupt, ' \
                                 f'player {active_player.get_user_id()} can spin.'
            case UserStatus.gaFreeTurn:
                status_active = UserStatus.psSpinAgain
                status_message = f'Player {active_player.get_user_id()} landed on Free Turn, token +1, spin again.'
            case UserStatus.gaCheckToken:
                status_active = UserStatus.psCheckToken
                if self.answer_result is None:  # Lose turn
                    if active_player.token <= 0:
                        status_message = f'Player {active_player.get_user_id()} landed on Lose Turn but has no token.'
                        self.active_player_index = (self.active_player_index + 1) % len(self.players)
                        active_player = self.players[self.active_player_index]
                        status_active = UserStatus.psSpin
                        non_active_players = [p for p in self.players if p != active_player]
                        for p in self.players:
                            p.set_status(UserStatus.usIdle)
                        status_message = f'{status_message} Player {active_player.get_user_id()} can spin.'
                    else:
                        active_player.use_token = None
                        status_message = f'Player {active_player.get_user_id()} landed on Lose Turn, checking token.'
                elif self.answer_result is False:  # Answered incorrectly
                    if active_player.token <= 0:
                        status_message = f'Incorrect, the answer is {self.question.answer}, ' \
                                         f'player {active_player.get_user_id()} has no token.'
                        self.active_player_index = (self.active_player_index + 1) % len(self.players)
                        active_player = self.players[self.active_player_index]
                        status_active = UserStatus.psSpin
                        non_active_players = [p for p in self.players if p != active_player]
                        for p in self.players:
                            p.set_status(UserStatus.usIdle)
                        status_message = f'{status_message} Player {active_player.get_user_id()} can spin.'
                    else:
                        active_player.use_token = None
                        status_message = f'Incorrect, the answer is {self.question.answer}, ' \
                                         f'checking token for player {active_player.get_user_id()}.'
            case UserStatus.gaPlayerChoice:
                status_active = UserStatus.psPlayerChoice
                active_player.category = -1
                status_message = f'Player {active_player.get_user_id()} landed on Player\'s Choice, ' \
                                 f'please pick a category.'
            case UserStatus.gaOpponentChoice:
                status_active = UserStatus.psOpponentChoice
                self.player_awaiting_opponent = \
                    self.players[(self.active_player_index + len(self.players) - 1) % len(self.players)]
                active_player.category = -1
                status_message = f'Player {self.player_awaiting_opponent.get_user_id()} landed on Opponent\'s Choice, ' \
                                 f'Player {active_player.get_user_id()} please pick a category.'
            case UserStatus.gaNothing:
                status_message = f'Nothing'
                pass
            case _:
                status_message = f'Error: Bad game action'
                pass

        # ##### Logic to check if game is over #####
        # TODO: update logic
        print(f'spin_counter = {self.spin_counter}')
        active_player_user_id = active_player.user_id
        if self.round_counter == 1:
            question_set = self.question_set1
        else:
            question_set = self.question_set2
        if ((status_active == UserStatus.psSpin or status_active == UserStatus.psSpinAgain) and
                (self.spin_counter <= 0 or question_set.has_unanswered_question() is False)):
            self.spin_result = -1
            self.round_counter += 1
            if self.round_counter == 2:
                self.spin_counter = self.CONST_SPIN_COUNTER
                self.wheel = Wheel(self.question_set2.get_list_of_categories())
                status_message = f"{status_message}\nRound 1 is over, beginning round 2. " \
                                 f"Player {active_player.get_user_id()} can spin."
                status_inactive = UserStatus.psWait
                status_active = UserStatus.psSpin
                # Reset Tokens for Round 2
                for p in self.players:
                    p.token = 0
            else:
                active_player_user_id = -1
                status_message = f'{status_message}\nGame Over. {self.scoreboard.find_winner()}'
                status_inactive = UserStatus.psIdle
                status_active = UserStatus.psIdle
            print(f'{status_message}')

            # for p in self.players:
            #     p.set_status(UserStatus.usIdle)

        status_message = f'[{datetime.now().strftime("%H:%M:%S")}] {status_message}'
        # ##### Send Status to inactive players #####
        status_packet = StatusPacket(
            active_player_user_id, status_message, status_inactive, 0, self.round_counter,
            self.spin_counter, self.spin_result, self.answer_result,
            self.players[0].user_id, self.players[0].score1, self.players[0].score2, self.players[0].token,
            self.players[1].user_id, self.players[1].score1, self.players[1].score2, self.players[1].token,
            self.players[2].user_id, self.players[2].score1, self.players[2].score2, self.players[2].token)
        command = Command(Ct.cmdStatusPacket, status_packet, 0)
        if self.player_awaiting_opponent is None:
            for p in non_active_players:
                self.client_command_issuer.send_command(p.get_user_id(), command)
        else:
            not_chosen_inactive_players = [p for p in non_active_players if p != self.player_awaiting_opponent]
            for p in not_chosen_inactive_players:
                self.client_command_issuer.send_command(p.get_user_id(), command)
            status_packet.status = UserStatus.psOpponentChoice
            command = Command(Ct.cmdStatusPacket, status_packet, 0)
            self.client_command_issuer.send_command(self.player_awaiting_opponent.get_user_id(), command)

        # ##### Send Status to active player #####
        status_packet_active = StatusPacket(
            active_player_user_id, status_message, status_active, 0, self.round_counter,
            self.spin_counter, self.spin_result, self.answer_result,
            self.players[0].user_id, self.players[0].score1, self.players[0].score2, self.players[0].token,
            self.players[1].user_id, self.players[1].score1, self.players[1].score2, self.players[1].token,
            self.players[2].user_id, self.players[2].score1, self.players[2].score2, self.players[2].token)
        command = Command(Ct.cmdStatusPacket, status_packet_active, 0)
        self.client_command_issuer.send_command(active_player.user_id, command)

        self.token_result = None
        # ##### State Transition #####
        if status_active == UserStatus.psIdle:  # Game Over
            # self.game_over()
            with self._lock:
                self.next_state = ServerStateTransition.game_over
        else:
            # self.await_response()
            with self._lock:
                self.next_state = ServerStateTransition.await_response

    def on_enter_state_await_player_response(self):
        print(self.current_state)
        active_player = self.players[self.active_player_index]
        while active_player.get_status() == UserStatus.usIdle:
            time.sleep(0.1)
        if active_player.get_status() == UserStatus.usSpin:
            # self.spin_wheel()
            with self._lock:
                self.next_state = ServerStateTransition.spin_wheel
        elif active_player.get_status() == UserStatus.usAnswer:
            # self.answer()
            with self._lock:
                self.next_state = ServerStateTransition.answer
        elif active_player.get_status() == UserStatus.usPickCategory:
            question_set = None
            self.game_action = UserStatus.gaAnswer
            if self.round_counter == 1:
                question_set = self.question_set1
            elif self.round_counter == 2:
                question_set = self.question_set2
            if question_set is not None:
                self.question = question_set.get_question(question_set.categories[active_player.category])
                if self.question is None:
                    # TODO: Shouldn't happen
                    # self.game_action = UserStatus.gaCategoryCompleted
                    pass
                else:
                    print(f'question = {self.question.question}')

            with self._lock:
                self.next_state = ServerStateTransition.pick_category
        elif active_player.get_status() == UserStatus.usUseToken:
            self.game_action = UserStatus.gaSpin
            self.answer_result = None
            self.token_result = active_player.use_token
            if active_player.use_token is True:
                active_player.token -= 1
                with self._lock:
                    self.next_state = ServerStateTransition.use_token
            elif active_player.use_token is False:
                with self._lock:
                    self.next_state = ServerStateTransition.not_use_token

    def on_enter_state_spin_wheel(self):
        print(self.current_state)
        active_player = self.players[self.active_player_index]
        active_player.category = -1
        self.player_awaiting_opponent = None
        while active_player.get_status() != UserStatus.usSpin:
            time.sleep(0.1)
        self.question = None
        self.answer_result = None
        self.spin_result = self.wheel.spin()
        self.spin_counter -= 1
        print(f'spin_result = {self.spin_result}')
        # if random.choice([True, False, False]):
        #     self.spin_result = 7
        #     print(f'[Testing Only] spin_result overwritten as {self.spin_result}')
        match self.spin_result:
            case 0 | 1 | 2 | 3 | 4 | 5 | 9 | 10 | 11 | 12 | 13 | 14:
                question_set = None
                self.game_action = UserStatus.gaAnswer
                # print(f'self.round_counter = {self.round_counter}')
                if self.round_counter == 1:
                    question_set = self.question_set1
                elif self.round_counter == 2:
                    question_set = self.question_set2
                # print(f'question_set = {question_set}')
                if question_set is not None:
                    self.question = question_set.get_question(question_set.categories[self.spin_result % 9])
                    if self.question is None:
                        self.game_action = UserStatus.gaCategoryCompleted
                    else:
                        print(f'question = {self.question.question}')

                # self.sector_category()
                with self._lock:
                    self.next_state = ServerStateTransition.sector_category
            # case 6:  # 7 | 8 | 15 | 16 | 17:  # Hack for Minimal Demo to eliminate harder sectors
            #     self.spin_result = 0
            #
            #     question_set = None
            #     self.game_action = UserStatus.gaAnswer
            #     # print(f'self.round_counter = {self.round_counter}')
            #     if self.round_counter == 1:
            #         question_set = self.question_set1
            #     elif self.round_counter == 2:
            #         question_set = self.question_set2
            #     # print(f'question_set = {question_set}')
            #     if question_set is not None:
            #         self.question = question_set.get_question(question_set.categories[self.spin_result % 9])
            #         if self.question is None:
            #             self.game_action = UserStatus.gaCategoryCompleted
            #         else:
            #             print(f'question = {self.question.question}')
            #
            #     # self.sector_category()
            #     with self._lock:
            #         self.next_state = ServerStateTransition.sector_category
            case 6:  # Free Turn
                self.game_action = UserStatus.gaFreeTurn
                active_player.token += 1
                with self._lock:
                    self.next_state = ServerStateTransition.sector_spin_to_sync
            case 7:  # Lose Turn
                self.game_action = UserStatus.gaCheckToken
                self.answer_result = None
                with self._lock:
                    self.next_state = ServerStateTransition.sector_spin_to_sync
            case 8:  # Bankrupt
                self.scoreboard.bankrupt(active_player.get_user_id(), self.round_counter)
                self.game_action = UserStatus.gaBankrupt
                with self._lock:
                    self.next_state = ServerStateTransition.sector_change_player
            case 15:  # Player's Choice
                self.game_action = UserStatus.gaPlayerChoice
                with self._lock:
                    self.next_state = ServerStateTransition.sector_spin_to_sync
            case 16:  # Opponents' Choice
                self.game_action = UserStatus.gaOpponentChoice
                with self._lock:
                    self.next_state = ServerStateTransition.sector_change_player
            case 17:  # Spin Again
                self.game_action = UserStatus.gaSpinAgain
                with self._lock:
                    self.next_state = ServerStateTransition.sector_spin_to_sync
        # q = self.question_set1.get_question(self.spin_result)
        # print(f'Question: {q.question}')
        # print(f'Options - A: {q.option_A}, B: {q.option_B}, C: {q.option_C}')
        # command = Command(Ct.cmdQuestion, q, 0)
        # self.client_command_issuer.send_command(active_player.get_user_id(), command)

    def on_enter_state_sector_category(self):
        print(self.current_state)
        # self.show_question()
        with self._lock:
            self.next_state = ServerStateTransition.show_question

    def on_enter_state_answer(self):
        print(self.current_state)
        active_player = self.players[self.active_player_index]
        while active_player.get_status() != UserStatus.usAnswer:
            time.sleep(0.1)

        match active_player.get_answer():
            case 0:
                selected_answer = 'A'
            case 1:
                selected_answer = 'B'
            case 2:
                selected_answer = 'C'
            case _:
                selected_answer = '.'
        self.question.isAnswered = True
        active_player.set_answer(None)

        if selected_answer == self.question.answer:
            print(f'{selected_answer} is correct!')
            self.game_action = UserStatus.gaSpin
            self.answer_result = True
            self.scoreboard.update_round_score(self.question.value, active_player.get_user_id(), self.round_counter)
            # self.answer_correct()
            with self._lock:
                self.next_state = ServerStateTransition.answer_correct
        else:
            print(f'{selected_answer} is incorrect.')
            self.game_action = UserStatus.gaCheckToken
            self.answer_result = False
            self.scoreboard.update_round_score(-self.question.value, active_player.get_user_id(), self.round_counter)
            # self.answer_incorrect()
            with self._lock:
                self.next_state = ServerStateTransition.answer_incorrect

    def on_enter_state_game_over(self):
        print(self.current_state)
        for p in self.players:
            p.set_status(UserStatus.usIdle)
        with self._lock:
            self.next_state = ServerStateTransition.back_to_lobby

    # def on_launch(self):
    #     print('Launching')
    #     print(self.current_state)


if __name__ == '__main__':
    ssm = ServerStateMachine()
    ssm.start()

    # print('done')
    # print(ssm.current_state)
    # print(ssm.is_state_fill_lobby)
