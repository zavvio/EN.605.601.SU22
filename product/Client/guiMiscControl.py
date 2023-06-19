import threading
from functools import partial

import PIL
import random
import time
from datetime import datetime
from PIL import Image
from PIL import ImageTk
from tkinter import *
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct


class MiscControl(object):
    def __init__(self, root, wheel_spinner, client_state_machine, status_panel):
        self.root = root
        self.wheel_spinner = wheel_spinner
        self.client_state_machine = client_state_machine
        self.status_panel = status_panel
        self.frame_misc_control = Frame(self.root)
        self.button_spin = Button(self.frame_misc_control, text="Spin", command=self.wheel_spinner.spin)
        self.button_spin.pack()
        self.button_ready = Button(self.frame_misc_control, text="Ready", command=self.get_ready)
        self.button_ready.pack()
        self.button_use_token = Button(self.frame_misc_control, text="Use Token",
                                       command=partial(self.send_token_decision, True))
        self.button_use_token.pack()
        self.button_not_use_token = Button(self.frame_misc_control, text="Don't Use Token",
                                           command=partial(self.send_token_decision, False))
        self.button_not_use_token.pack()
        self.root.add(self.frame_misc_control)
        thread_misc = threading.Thread(target=self.daemon_update_misc, daemon=True)
        thread_misc.start()

    def daemon_update_misc(self):
        while True:
            if (self.client_state_machine.scr.active_player_id == self.client_state_machine.user_id
                    and self.client_state_machine.is_state_spin_wheel):
                self.button_spin.config(state=NORMAL)
            else:
                self.button_spin.config(state=DISABLED)  # , bg='grey')
            if not self.client_state_machine.is_ready:
                self.button_ready.config(state=NORMAL)
            if self.client_state_machine.is_state_check_token:
                self.button_use_token.config(state=NORMAL)
                self.button_not_use_token.config(state=NORMAL)
            else:
                self.button_use_token.config(state=DISABLED)
                self.button_not_use_token.config(state=DISABLED)
            time.sleep(0.1)

    def get_ready(self):
        self.client_state_machine.is_ready = True
        self.button_ready.config(state=DISABLED)  # , bg='grey')
        self.status_panel.set_msg_from_client('You\'re Ready.')
        self.client_state_machine.scr.status_msg = 'Awaiting players to join...\n'

    def send_token_decision(self, decision):
        self.client_state_machine.scr.token_decision = decision
        if decision is True:
            self.status_panel.set_msg_from_client(f'Using Token.')
        elif decision is False:
            self.status_panel.set_msg_from_client(f'Not using Token.')
        command = Command(Ct.cmdUseToken, decision, 0)
        self.client_state_machine.sci.send_command(command)
