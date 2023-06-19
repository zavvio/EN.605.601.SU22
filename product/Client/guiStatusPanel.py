import PIL
import random
import threading
import time
from datetime import datetime
from PIL import Image
from PIL import ImageTk
from tkinter import *

from product.Common.userStatus import UserStatus


class StatusPanel(object):
    def __init__(self, root, client_state_machine):
        self.root = root
        self.client_state_machine = client_state_machine
        self.label_status = Label(self.root)
        self.root.add(self.label_status)
        self.msg_from_client = 'Click "Ready" to get start...'
        self.msg_from_server = 'Awaiting players to join...\n'
        self.label_status.config(text=f'\n{self.msg_from_server}\n{self.msg_from_client}')
        thread_status = threading.Thread(target=self.daemon_update_status_msg, daemon=True)
        thread_status.start()

    def daemon_update_status_msg(self):
        while True:
            # self.set_msg_from_client()
            self.set_msg_from_server(self.client_state_machine.scr.status_msg)
            if (self.client_state_machine.scr.player_status == UserStatus.psIdle
                    and not self.client_state_machine.is_ready):
                self.set_msg_from_client('Click "Ready" to get start...')
            time.sleep(0.1)

    def set_msg_from_client(self, msg):
        self.msg_from_client = msg
        self.label_status.config(text=f'\n{self.msg_from_server}\n{self.msg_from_client}')

    def set_msg_from_server(self, msg):
        self.msg_from_server = msg
        self.label_status.config(text=f'\n{self.msg_from_server}\n{self.msg_from_client}')
