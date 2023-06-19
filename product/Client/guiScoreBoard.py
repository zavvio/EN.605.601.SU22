import threading

import PIL
import random
import time
from datetime import datetime
from functools import partial
from PIL import Image
from PIL import ImageTk
from tkinter import *


class ScoreBoard(object):
    def __init__(self, root, client_state_machine):
        self.root = root
        self.client_state_machine = client_state_machine
        self.frame_scoreboard = Frame(self.root)
        self.var_scoreboard = StringVar()
        self.var_scoreboard.set(f'\n##########   Scoreboard   ##########\n\n\n\n\n\n\n')
        self.label_scoreboard = Label(self.frame_scoreboard, textvariable=self.var_scoreboard)
        self.label_scoreboard.pack()
        self.root.add(self.frame_scoreboard)
        thread_scoreboard = threading.Thread(target=self.daemon_update_scoreboard, daemon=True)
        thread_scoreboard.start()

    def daemon_update_scoreboard(self):
        while True:
            self.var_scoreboard.set(
                f'\n##########   Scoreboard   ##########\n\n'
                f'Round: {self.client_state_machine.scr.round_num}\n'
                f'Remaining Spin: {self.client_state_machine.scr.remaining_spins}\n'
                f'Player {self.client_state_machine.scr.player_id_1}:\t'
                f'[round 1] {self.client_state_machine.scr.score1a}\t'
                f'[round 2] {self.client_state_machine.scr.score1b}\t'
                f'[token] {self.client_state_machine.scr.token1}\n'
                f'Player {self.client_state_machine.scr.player_id_2}:\t'
                f'[round 1] {self.client_state_machine.scr.score2a}\t'
                f'[round 2] {self.client_state_machine.scr.score2b}\t'
                f'[token] {self.client_state_machine.scr.token2}\n'
                f'Player {self.client_state_machine.scr.player_id_3}:\t'
                f'[round 1] {self.client_state_machine.scr.score3a}\t'
                f'[round 2] {self.client_state_machine.scr.score3b}\t'
                f'[token] {self.client_state_machine.scr.token3}\n')
            time.sleep(0.1)
