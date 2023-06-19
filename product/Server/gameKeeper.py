import time
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct
from product.Common.userStatus import UserStatus
from scoreboard import Scoreboard
from wheel import Wheel


class GameKeeper:
    def __init__(self, user_manager, players, client_command_issuer, question_set):
        self.wheel = Wheel(question_set.get_list_of_categories())
        self.round_counter = 0
        self.spin_counter = 50
        self.user_manager = user_manager
        self.players = players
        self.num_of_players = len(players)
        self.active_player_index = 0
        self.scoreboard = Scoreboard(user_manager, players)
        self.client_command_issuer = client_command_issuer
        self.question_set = question_set

    def play_game(self):
        active_player = self.players[self.active_player_index]
        # send spin wheel command
        # get wheel response
        while active_player.get_status() != UserStatus.usSpin:
            time.sleep(1)

        # Send a question to active player
        # Temp logic for getting an available question
        for turn in range(2):
            q = None
            while q is None:
                result = self.wheel.spin()
                while result not in self.question_set.get_list_of_categories():
                    # print(f'sector: {result}')
                    result = self.wheel.spin()
                print(f'Landed on wheel sector: {result}')
                q = self.question_set.get_question(result)

            print(f'Question: {q.question}')
            print(f'Options - A: {q.option_A}, B: {q.option_B}, C: {q.option_C}')
            command = Command(Ct.cmdQuestion, q, 0)
            self.client_command_issuer.send_command(active_player.get_user_id(), command)

            # Wait for answer from active player
            while active_player.get_status() != UserStatus.usAnswer:
                time.sleep(1)
            match active_player.get_answer():
                case 0:
                    selected_answer = 'A'
                case 1:
                    selected_answer = 'B'
                case 2:
                    selected_answer = 'C'
                case _:
                    selected_answer = '.'
            if selected_answer == q.answer:
                print(f'{selected_answer} is correct!')
                self.scoreboard.update_round_score(q.value, active_player.get_user_id())
            else:
                print(f'{selected_answer} is incorrect.')
            q.isAnswered = True
            active_player.set_status(0)
            active_player.set_answer(None)

        self.scoreboard.find_winner()
