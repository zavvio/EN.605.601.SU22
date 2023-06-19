import PIL
import random
import time
from datetime import datetime
from PIL import Image
from PIL import ImageTk
from tkinter import *

from product.Common.command import Command
from product.Common.commandType import CommandType as Ct


class WheelSpinner(object):
    def __init__(self, root, status_panel, filename, client_state_machine, **kwargs):
        self.root = root
        self.status_panel = status_panel
        self.filename = filename
        self.client_state_machine = client_state_machine
        self.canvas = Canvas(root, bg='khaki1', width=500, height=500)
        self.root.add(self.canvas)
        self.angle = 10
        self.image = PIL.Image.open(self.filename)
        self.image_tk = ImageTk.PhotoImage(self.image.rotate(self.angle))
        self.canvas_image = self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

        self.time_start = ...
        self.timeout = ...
        # self.is_spin_ready = ...
        # self.chosen_sector = ...
        # self.spin()

    def spin(self, timeout=2):
        if self.client_state_machine.user_id != self.client_state_machine.scr.active_player_id:
            return
        self.status_panel.set_msg_from_client(f'Sent spin request to server, awaiting result...')
        round_num = self.client_state_machine.scr.round_num
        self.request_spin_from_server()
        # while self.client_state_machine.scr.is_spin_ready is False:
        while (self.client_state_machine.user_id == self.client_state_machine.scr.active_player_id
               and self.client_state_machine.scr.chosen_sector == -1
               and round_num == self.client_state_machine.scr.round_num):
            time.sleep(0.1)
        # print(f'Landed on sector {self.client_state_machine.scr.chosen_sector}')
        self.status_panel.set_msg_from_client(f'Landed on sector {self.client_state_machine.scr.chosen_sector}')
        self.timeout = timeout
        self.time_start = datetime.now().timestamp()
        self.root.after(20, self.draw)  # update every 20ms

    def draw(self):
        self.angle += 20  # spinning anti-clockwise, i.e. sector is going clockwise; 360 / 18-sectors = 20 degree
        self.angle %= 360
        self.image = PIL.Image.open(self.filename)
        self.image_tk = ImageTk.PhotoImage(self.image.rotate(self.angle))
        self.canvas_image = self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)
        self.root.update_idletasks()
        if (datetime.now().timestamp() - self.time_start) < self.timeout:
            self.root.after(20, self.draw)
        else:
            self.angle = (10 + self.client_state_machine.scr.chosen_sector * 20) % 360
            self.image = PIL.Image.open(self.filename)
            self.image_tk = ImageTk.PhotoImage(self.image.rotate(self.angle))
            self.canvas_image = self.canvas.create_image(0, 0, anchor=NW, image=self.image_tk)

    def request_spin_from_server(self):
        # self.client_state_machine.scr.is_spin_ready = False
        self.client_state_machine.scr.chosen_sector = -1
        command = Command(Ct.cmdSpinWheel, self.client_state_machine.user_id, 0)
        if self.client_state_machine.sci.send_command(command) < 0:
            pass
        # while self.client_state_machine.scr.chosen_sector == -1:
        #     time.sleep(0.1)
        # self.client_state_machine.scr.is_spin_ready = True
