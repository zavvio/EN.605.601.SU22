import threading

import PIL
import random
import time
from datetime import datetime
from functools import partial
from PIL import Image
from PIL import ImageTk
from tkinter import *
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct
from product.Common.userStatus import UserStatus


class AnswerManager(object):
    def __init__(self, root, client_state_machine):
        self.root = root
        self.client_state_machine = client_state_machine
        # ### Radiobutton example ###
        self.frame_answer = Frame(self.root)
        self.var_answer = StringVar()
        self.var_answer.set('\nPlease choose your answer:')
        self.label_answer = Label(self.frame_answer, textvariable=self.var_answer)
        self.label_answer.pack()
        self.var = IntVar()
        self.R1 = Radiobutton(self.frame_answer, text="Option A", variable=self.var, value=0)  # , command=sel)
        self.R1.pack(anchor=W)
        self.R2 = Radiobutton(self.frame_answer, text="Option B", variable=self.var, value=1)  # , command=sel)
        self.R2.pack(anchor=W)
        self.R3 = Radiobutton(self.frame_answer, text="Option C", variable=self.var, value=2)  # , command=sel)
        self.R3.pack(anchor=W)
        self.button_submit_answer = Button(self.frame_answer, text="Submit", command=self.sel)
        self.button_submit_answer.pack()
        self.label = Label(self.frame_answer)
        self.label.pack()
        self.root.add(self.frame_answer)
        thread_answer = threading.Thread(target=self.daemon_update_answer, daemon=True)
        thread_answer.start()

    def daemon_update_answer(self):
        while True:
            # print('daemon_update_answer')
            question = self.client_state_machine.scr.question
            if question is not None:
                self.R1.config(text=question.option_A)
                self.R2.config(text=question.option_B)
                self.R3.config(text=question.option_C)
            if (self.client_state_machine.scr.active_player_id != self.client_state_machine.user_id
                    or self.client_state_machine.scr.player_status == UserStatus.psIdle
                    or self.client_state_machine.scr.player_status == UserStatus.psSpin
                    or self.client_state_machine.scr.player_status == UserStatus.psWait):
                self.button_submit_answer.config(state=DISABLED)  # , bg='grey')
            else:
                self.button_submit_answer.config(state=NORMAL)
            time.sleep(0.1)

    # ### Radiobutton example ###
    def sel(self):
        if 0 <= self.var.get() < 3:
            selection = "You selected answer " + str(self.var.get())
            self.label.config(text=selection)
            command = Command(Ct.cmdAnswer, self.var.get(), 0)
            self.client_state_machine.sci.send_command(command)
        else:
            self.label.config(text='Please select an answer')
