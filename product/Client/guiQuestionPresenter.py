import threading

import PIL
import random
import time
from datetime import datetime
from PIL import Image
from PIL import ImageTk
from tkinter import *


class QuestionPresenter(object):
    def __init__(self, root, client_state_machine):
        self.root = root
        self.client_state_machine = client_state_machine
        self.text_question = Text(self.root, height=10, width=80)
        self.text_question.insert(INSERT, 'This is Question pane')
        self.root.add(self.text_question)
        thread_question = threading.Thread(target=self.daemon_update_question, daemon=True)
        thread_question.start()

    def daemon_update_question(self):
        while True:
            # print('daemon_update_question')
            if self.client_state_machine.scr.question is not None:
                self.show_question(self.client_state_machine.scr.question)
            time.sleep(0.1)

    def show_question(self, question):
        self.text_question.delete(1.0, END)
        if type(question) == int:
            self.text_question.insert(INSERT, f'Showing question {question}')
        else:
            self.text_question.insert(INSERT, f'{question.question}')
        # self.question_board_buttons[index].config(state=DISABLED)
