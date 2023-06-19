import os
import random
import threading
import time
from functools import partial
from tkinter import *
from product.Client.guiAnswerManager import AnswerManager
from product.Client.guiMiscControl import MiscControl
from product.Client.guiQuestionBoard import QuestionBoard
from product.Client.guiQuestionPresenter import QuestionPresenter
from product.Client.guiScoreBoard import ScoreBoard
from product.Client.guiStatusPanel import StatusPanel
from product.Client.guiWheelSpinner import WheelSpinner


class GuiManager:
    def __init__(self, client_state_machine):
        self.client_state_machine = client_state_machine
        self.root = Tk()
        self.root.title(f'Wheel of Jeopardy! --- Gameshow Geeks [Player {self.client_state_machine.user_id}]')

        # ### PanedWindow example ###
        self.base_pane = PanedWindow(self.root)
        self.base_pane.pack(fill=BOTH, expand=1)

        self.left_pane = PanedWindow(self.base_pane, orient=VERTICAL)
        self.base_pane.add(self.left_pane)

        self.status_panel = StatusPanel(self.left_pane, self.client_state_machine)
        path = os.getcwd()
        if path.endswith('Client'):
            path = '../../resource/wheel.png'
        else:
            path = 'resource/wheel.png'
        self.wheel_spinner = WheelSpinner(self.left_pane, self.status_panel, path, self.client_state_machine)
        self.question_presenter = QuestionPresenter(self.left_pane, self.client_state_machine)

        self.right_pane = PanedWindow(self.base_pane, orient=VERTICAL)
        self.base_pane.add(self.right_pane)

        self.question_board = QuestionBoard(self.right_pane, self.question_presenter, self.client_state_machine,
                                            self.status_panel)
        self.score_board = ScoreBoard(self.right_pane, self.client_state_machine)
        self.answer_manager = AnswerManager(self.right_pane, self.client_state_machine)
        self.misc_control = MiscControl(self.right_pane, self.wheel_spinner, self.client_state_machine,
                                        self.status_panel)

        # thread1 = threading.Thread(target=self.root.mainloop)
        # thread1.start()
        self.root.mainloop()


if __name__ == '__main__':
    gui_manager = GuiManager()
