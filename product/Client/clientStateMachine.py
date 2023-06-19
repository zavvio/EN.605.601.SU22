import threading
import time
from enum import Enum

from statemachine import StateMachine, State
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct
from product.Common.userStatus import UserStatus


class ClientStateTransition(Enum):
    start_sm = 1
    ready = 2
    begin = 3
    spin_wheel = 4
    game_over = 5
    wait_to_check_token = 6
    sector_category = 7
    sector_category_done = 8
    sector_spin_to_wait = 9
    sector_spin_to_pick = 10
    sector_spin_to_wait_for_pick = 11
    sector_spin_to_check_token = 12
    answer_self_pick = 13
    answer_opponent_pick = 14
    answer = 15
    answer_correct = 16
    answer_game_over = 17
    answer_incorrect = 18
    submit_token_decision = 19
    pick_for_opponent = 20
    done_picking_for_opponent = 21


class ClientStateMachine(StateMachine, threading.Thread):
    state_start = State('Start State Machine', initial=True)
    state_idle = State('Idle')
    state_ready = State('Ready')
    state_wait = State('Wait')
    state_spin_wheel = State('Spin Wheel')
    state_sector_category = State('Sector: Category')
    state_player_choice = State('Sector: Player\'s Choice')
    state_opponent_choice = State('Sector: Opponent\'s Choice')
    state_answer = State('Answer')
    state_pick_for_opponent = State('Pick Category for Opponent')
    state_check_token = State('Check Token')
    # joined = State('Joined', initial=True)
    # ready = State('Ready')
    # idle = State('Idle')
    # turn_player = State('Turn player')
    #
    # ready_up = joined.to(ready)
    # start = ready.to(idle)
    # activate = idle.to(turn_player)
    # deactivate = turn_player.to(idle)
    start_sm = state_start.to(state_idle)
    ready = state_idle.to(state_ready)
    begin = state_ready.to(state_wait)
    spin_wheel = state_wait.to(state_spin_wheel)
    game_over = state_wait.to(state_idle)
    wait_to_check_token = state_wait.to(state_check_token)
    sector_category = state_spin_wheel.to(state_sector_category)
    sector_category_done = state_sector_category.to(state_wait)
    sector_spin_to_wait = state_spin_wheel.to(state_wait)
    sector_spin_to_pick = state_spin_wheel.to(state_player_choice)
    sector_spin_to_wait_for_pick = state_spin_wheel.to(state_opponent_choice)
    sector_spin_to_check_token = state_spin_wheel.to(state_check_token)
    answer_self_pick = state_player_choice.to(state_answer)
    answer_opponent_pick = state_opponent_choice.to(state_answer)
    answer = state_sector_category.to(state_answer)
    answer_correct = state_answer.to(state_spin_wheel)
    answer_game_over = state_answer.to(state_wait)
    answer_incorrect = state_answer.to(state_check_token)
    submit_token_decision = state_check_token.to(state_wait)
    pick_for_opponent = state_wait.to(state_pick_for_opponent)
    done_picking_for_opponent = state_pick_for_opponent.to(state_wait)

    def __init__(self, user_id, server_command_issuer, server_command_receiver):
        threading.Thread.__init__(self, daemon=True)
        self._lock = threading.Lock()
        self.curr_state = ...
        self.next_state = ...
        self.user_id = user_id
        self.sci = server_command_issuer
        self.scr = server_command_receiver
        self.scr.user_id = user_id
        self.is_ready = False
        self.cached_remaining_spins = -1
        # print('__init__')

    def run(self):
        # print('run...')
        super(ClientStateMachine, self).__init__()
        self.start_sm()
        while True:
            time.sleep(0.1)
            # print(f'daemon_client_state_machine')
            # print(f'{self.curr_state} ... {self.next_state}')
            if self.curr_state == self.next_state:
                # print(f'{self.curr_state} == {self.next_state}')
                continue
            with self._lock:
                self.curr_state = self.next_state
                # print(f'{self.curr_state} <-- {self.next_state}')
            match self.curr_state:
                case ClientStateTransition.ready:
                    self.ready()
                case ClientStateTransition.begin:
                    self.begin()
                case ClientStateTransition.spin_wheel:
                    self.spin_wheel()
                case ClientStateTransition.game_over:
                    self.game_over()
                case ClientStateTransition.wait_to_check_token:
                    self.wait_to_check_token()
                case ClientStateTransition.sector_category:
                    self.sector_category()
                case ClientStateTransition.sector_category_done:
                    self.sector_category_done()
                case ClientStateTransition.sector_spin_to_wait:
                    self.sector_spin_to_wait()
                case ClientStateTransition.sector_spin_to_pick:
                    self.sector_spin_to_pick()
                case ClientStateTransition.sector_spin_to_wait_for_pick:
                    self.sector_spin_to_wait_for_pick()
                case ClientStateTransition.sector_spin_to_check_token:
                    self.sector_spin_to_check_token()
                case ClientStateTransition.answer_self_pick:
                    self.answer_self_pick()
                case ClientStateTransition.answer_opponent_pick:
                    self.answer_opponent_pick()
                case ClientStateTransition.answer:
                    self.answer()
                case ClientStateTransition.answer_correct:
                    self.answer_correct()
                case ClientStateTransition.answer_game_over:
                    self.answer_game_over()
                case ClientStateTransition.answer_incorrect:
                    self.answer_incorrect()
                case ClientStateTransition.submit_token_decision:
                    self.submit_token_decision()
                case ClientStateTransition.pick_for_opponent:
                    self.pick_for_opponent()
                case ClientStateTransition.done_picking_for_opponent:
                    self.done_picking_for_opponent()

    def on_enter_state_idle(self):
        # print('Idling...')
        print(self.current_state)
        self.is_ready = False
        self.scr.player_status = UserStatus.psIdle

        print('Not ready...')
        while not self.is_ready:
            time.sleep(1)

        command = Command(Ct.cmdReady, self.user_id, 0)
        if self.sci.send_command(command) < 0:
            pass
        # self.ready()
        with self._lock:
            self.next_state = ClientStateTransition.ready

    def on_enter_state_ready(self):
        print('Ready...')
        print(self.current_state)
        while self.scr.player_status == UserStatus.psIdle:
            time.sleep(0.1)
        # self.begin()
        with self._lock:
            self.next_state = ClientStateTransition.begin

    def on_enter_state_wait(self):
        # print('Wait...')
        print(self.current_state)
        while self.scr.player_status == UserStatus.psWait:
            time.sleep(0.1)
            # show question for inactive players
            if (type(self.scr.chosen_sector) == int
                    and self.scr.chosen_sector != -1
                    and (self.cached_remaining_spins != self.scr.remaining_spins
                         or self.scr.show_question_from_picking)):
                self.cached_remaining_spins = self.scr.remaining_spins
                if self.scr.show_question_from_picking:
                    print(f'Picked category: {self.scr.chosen_sector}')
                    self.scr.show_question_from_picking = False
                question_set = None
                if self.scr.round_num == 1:
                    question_set = self.scr.question_set1
                elif self.scr.round_num == 2:
                    question_set = self.scr.question_set2
                if question_set is not None:
                    if (self.scr.chosen_sector % 9) < 6:
                        self.scr.question = question_set.get_question(question_set.categories[self.scr.chosen_sector % 9])
                        if self.scr.question is not None:
                            self.scr.question.isAnswered = True

        match self.scr.player_status:
            case UserStatus.psIdle:
                with self._lock:
                    self.next_state = ClientStateTransition.game_over
            case UserStatus.psSpin:
                # self.spin_wheel()
                with self._lock:
                    self.next_state = ClientStateTransition.spin_wheel
            case UserStatus.psOpponentChoice:
                with self._lock:
                    self.next_state = ClientStateTransition.pick_for_opponent
            case UserStatus.psCheckToken:
                with self._lock:
                    self.next_state = ClientStateTransition.wait_to_check_token
            case UserStatus.psGameOver:
                pass
            case _:
                pass

    def on_enter_state_spin_wheel(self):
        # print('Spin Wheel...')
        print(self.current_state)
        self.scr.player_status = UserStatus.psUnknown
        # while (self.scr.player_status != UserStatus.psShowQuestion
        #         and self.scr.player_status != UserStatus.psSpin
        #         and self.scr.player_status != UserStatus.psSpinAgain
        #         and self.scr.player_status != UserStatus.psWait
        #         and self.scr.player_status != UserStatus.psIdle):
        while self.scr.player_status == UserStatus.psUnknown:
            time.sleep(0.1)
        self.cached_remaining_spins = self.scr.remaining_spins
        # self.sector_category()
        with self._lock:
            if (self.scr.player_status == UserStatus.psSpinAgain or
                    self.scr.player_status == UserStatus.psSpin):
                self.scr.player_status = UserStatus.psSpin
                self.next_state = ClientStateTransition.sector_spin_to_wait
            elif (self.scr.player_status == UserStatus.psWait or
                  self.scr.player_status == UserStatus.psIdle):
                self.next_state = ClientStateTransition.sector_spin_to_wait
            elif self.scr.player_status == UserStatus.psPlayerChoice:
                self.next_state = ClientStateTransition.sector_spin_to_pick
            elif self.scr.player_status == UserStatus.psOpponentChoice:
                self.next_state = ClientStateTransition.sector_spin_to_wait_for_pick
            elif self.scr.player_status == UserStatus.psCheckToken:
                self.next_state = ClientStateTransition.sector_spin_to_check_token
            else:
                self.next_state = ClientStateTransition.sector_category

    def on_enter_state_sector_category(self):
        # print('Sector Category...')
        print(self.current_state)
        question_set = None
        if self.scr.round_num == 1:
            question_set = self.scr.question_set1
        elif self.scr.round_num == 2:
            question_set = self.scr.question_set2
        if question_set is not None:
            self.scr.question = question_set.get_question(question_set.categories[self.scr.chosen_sector % 9])
            if self.scr.question is None:
                # self.sector_category_done()
                with self._lock:
                    self.next_state = ClientStateTransition.sector_category_done
            else:
                self.scr.question.isAnswered = True
                # self.answer()
                with self._lock:
                    self.next_state = ClientStateTransition.answer

    def on_enter_state_answer(self):
        # print('Answering...')
        print(self.current_state)
        self.scr.answer_result = None
        while self.scr.answer_result is None:
            time.sleep(0.1)
        if self.scr.answer_result:
            # self.answer_correct()
            with self._lock:
                if self.scr.player_status == UserStatus.psIdle:
                    # Answered correctly but game is over
                    self.next_state = ClientStateTransition.answer_game_over
                else:
                    self.next_state = ClientStateTransition.answer_correct
        else:
            token = 0
            if self.scr.user_id == self.scr.player_id_1:
                token = self.scr.token1
            elif self.scr.user_id == self.scr.player_id_2:
                token = self.scr.token2
            elif self.scr.user_id == self.scr.player_id_3:
                token = self.scr.token3
            with self._lock:
                if token > 0:
                    self.next_state = ClientStateTransition.answer_incorrect
                else:  # No token available, go back to wait
                    self.next_state = ClientStateTransition.answer_game_over

    def on_enter_state_check_token(self):
        print(self.current_state)
        self.scr.token_decision = None
        while self.scr.token_decision is None:
            time.sleep(0.1)
        with self._lock:
            self.next_state = ClientStateTransition.submit_token_decision

    def on_enter_state_player_choice(self):
        print(self.current_state)
        # self.scr.answer_result = None
        # while self.scr.answer_result is None:
        #     time.sleep(0.1)
        self.scr.pick_category = -1
        while self.scr.pick_category == -1:
            time.sleep(0.5)

        question_set = None
        if self.scr.round_num == 1:
            question_set = self.scr.question_set1
        elif self.scr.round_num == 2:
            question_set = self.scr.question_set2
        if question_set is not None:
            self.scr.question = question_set.get_question(question_set.categories[self.scr.pick_category])
            if self.scr.question is None:
                # Shouldn't happen
                # with self._lock:
                #     self.next_state = ClientStateTransition.sector_category_done
                pass
            else:
                self.scr.question.isAnswered = True

        with self._lock:
            self.next_state = ClientStateTransition.answer_self_pick

    def on_enter_state_opponent_choice(self):
        print(self.current_state)
        self.scr.chosen_sector = -1
        while self.scr.chosen_sector == -1:
            time.sleep(0.5)

        question_set = None
        if self.scr.round_num == 1:
            question_set = self.scr.question_set1
        elif self.scr.round_num == 2:
            question_set = self.scr.question_set2
        if question_set is not None:
            self.scr.question = question_set.get_question(question_set.categories[self.scr.chosen_sector % 9])
            if self.scr.question is None:
                # Shouldn't happen
                # with self._lock:
                #     self.next_state = ClientStateTransition.sector_category_done
                pass
            else:
                self.scr.question.isAnswered = True

        with self._lock:
            self.next_state = ClientStateTransition.answer_opponent_pick

    def on_enter_state_pick_for_opponent(self):
        print(self.current_state)
        self.scr.player_status = UserStatus.psWait
        self.scr.pick_category = -1
        while self.scr.pick_category == -1:
            time.sleep(0.5)

        # question_set = None
        # if self.scr.round_num == 1:
        #     question_set = self.scr.question_set1
        # elif self.scr.round_num == 2:
        #     question_set = self.scr.question_set2
        # if question_set is not None:
        #     self.scr.question = question_set.get_question(question_set.categories[self.scr.pick_category])
        #     if self.scr.question is None:
        #         # Shouldn't happen
        #         # with self._lock:
        #         #     self.next_state = ClientStateTransition.sector_category_done
        #         pass
        #     else:
        #         # self.scr.question.isAnswered = True
        #         pass
        with self._lock:
            self.next_state = ClientStateTransition.done_picking_for_opponent
