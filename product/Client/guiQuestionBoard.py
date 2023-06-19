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


class QuestionBoard(object):
    def __init__(self, root, question_presenter, client_state_machine, status_panel):
        self.root = root
        self.question_presenter = question_presenter
        self.client_state_machine = client_state_machine
        self.status_panel = status_panel
        self.frame_question_board = Frame(self.root)
        self.cached_round_num = -1

        # Creating Categories
        self.var_category_1 = StringVar()
        self.var_category_2 = StringVar()
        self.var_category_3 = StringVar()
        self.var_category_4 = StringVar()
        self.var_category_5 = StringVar()
        self.var_category_6 = StringVar()
        self.category_buttons = {0: Button(self.frame_question_board, textvariable=self.var_category_1, bg='khaki3',
                                           width=10, borderwidth=5, command=partial(self.pick_category, 0)),
                                 1: Button(self.frame_question_board, textvariable=self.var_category_2, bg='khaki3',
                                           width=10, borderwidth=5, command=partial(self.pick_category, 1)),
                                 2: Button(self.frame_question_board, textvariable=self.var_category_3, bg='khaki3',
                                           width=10, borderwidth=5, command=partial(self.pick_category, 2)),
                                 3: Button(self.frame_question_board, textvariable=self.var_category_4, bg='khaki3',
                                           width=10, borderwidth=5, command=partial(self.pick_category, 3)),
                                 4: Button(self.frame_question_board, textvariable=self.var_category_5, bg='khaki3',
                                           width=10, borderwidth=5, command=partial(self.pick_category, 4)),
                                 5: Button(self.frame_question_board, textvariable=self.var_category_6, bg='khaki3',
                                           width=10, borderwidth=5, command=partial(self.pick_category, 5))}
        # self.category_buttons[0] = Label(self.frame_question_board, textvariable=self.var_category_1,
        #                               width=10, bd=6, bg='khaki3', relief=RAISED)
        # self.category_buttons[1] = Label(self.frame_question_board, textvariable=self.var_category_2,
        #                               width=10, bd=6, bg='khaki3', relief=RAISED)
        # self.category_buttons[2] = Label(self.frame_question_board, textvariable=self.var_category_3,
        #                               width=10, bd=6, bg='khaki3', relief=RAISED)
        # self.category_buttons[3] = Label(self.frame_question_board, textvariable=self.var_category_4,
        #                               width=10, bd=6, bg='khaki3', relief=RAISED)
        # self.category_buttons[4] = Label(self.frame_question_board, textvariable=self.var_category_5,
        #                               width=10, bd=6, bg='khaki3', relief=RAISED)
        # self.category_buttons[5] = Label(self.frame_question_board, textvariable=self.var_category_6,
        #                               width=10, bd=6, bg='khaki3', relief=RAISED)
        self.var_category_1.set('\nCategory A\n')
        self.var_category_2.set('\nCategory B\n')
        self.var_category_3.set('\nCategory C\n')
        self.var_category_4.set('\nCategory D\n')
        self.var_category_5.set('\nCategory E\n')
        self.var_category_6.set('\nCategory F\n')
        self.category_buttons[0].grid(row=0, column=0)
        self.category_buttons[1].grid(row=0, column=1)
        self.category_buttons[2].grid(row=0, column=2)
        self.category_buttons[3].grid(row=0, column=3)
        self.category_buttons[4].grid(row=0, column=4)
        self.category_buttons[5].grid(row=0, column=5)

        # Creating Questions
        self.question_board_buttons = {}
        b = 0
        for c in range(6):
            for r in range(1, 6):
                b = b + 1
                match c:
                    case 0:
                        text_question_button = f'A{r} ${r*200}'
                    case 1:
                        text_question_button = f'B{r} ${r*200}'
                    case 2:
                        text_question_button = f'C{r} ${r*200}'
                    case 3:
                        text_question_button = f'D{r} ${r*200}'
                    case 4:
                        text_question_button = f'E{r} ${r*200}'
                    case 5:
                        text_question_button = f'F{r} ${r*200}'
                    case _:
                        text_question_button = ''
                self.btn_question = Button(self.frame_question_board, text=text_question_button, bg='khaki4',
                                           width=10, borderwidth=5, command=partial(self.show_question, b))
                # print(f'b = {b}, text_question = {text_question_button}')
                self.question_board_buttons[b] = self.btn_question
                self.btn_question.grid(row=r, column=c)

        self.root.add(self.frame_question_board)
        thread_question_board = threading.Thread(target=self.daemon_update_question_board, daemon=True)
        thread_question_board.start()

    def daemon_update_question_board(self):
        while True:
            if 3 > self.client_state_machine.scr.round_num != self.cached_round_num:
                self.cached_round_num = self.client_state_machine.scr.round_num
                self.reset_board()
            # Updates related to category
            categories = None
            qs = None
            if self.client_state_machine.scr.round_num == 1 and self.client_state_machine.scr.question_set1 is not None:
                categories = self.client_state_machine.scr.question_set1.categories
                qs = self.client_state_machine.scr.question_set1
            elif self.client_state_machine.scr.round_num == 2 and self.client_state_machine.scr.question_set2 is not None:
                categories = self.client_state_machine.scr.question_set2.categories
                qs = self.client_state_machine.scr.question_set2
            if categories is not None:
                # print(f'Categories = {categories}')
                self.var_category_1.set(f'Category A\n{categories[0]}\n')
                self.var_category_2.set(f'Category B\n{categories[1]}\n')
                self.var_category_3.set(f'Category C\n{categories[2]}\n')
                self.var_category_4.set(f'Category D\n{categories[3]}\n')
                self.var_category_5.set(f'Category E\n{categories[4]}\n')
                self.var_category_6.set(f'Category F\n{categories[5]}\n')

                category_done = qs.get_categories_status()
                for i in range(6):
                    if category_done[i] is True:
                        self.category_buttons[i].config(state=DISABLED, bg='grey')
                    else:
                        self.category_buttons[i].config(state=NORMAL, bg='khaki3')

            # Updates related to question selected
            question = self.client_state_machine.scr.question
            if question is not None:
                # print(f'[guiQuestionboard] question_id = {question.question_id}')
                self.question_board_buttons[question.question_id].config(state=DISABLED, bg='grey')
            time.sleep(0.1)

    def show_question(self, index):
        self.question_presenter.show_question(index)
        # self.question_board_buttons[index].config(state=DISABLED, bg='grey')

    def reset_board(self):
        self.client_state_machine.scr.question = None
        for i in range(1, 31):
            self.question_board_buttons[i].config(state=NORMAL, bg='khaki4')

    def pick_category(self, index):
        self.client_state_machine.scr.pick_category = index
        self.status_panel.set_msg_from_client(f'Selected category {index}.')
        command = Command(Ct.cmdPickCategory, index, 0)
        self.client_state_machine.sci.send_command(command)
