import threading
import time
from enum import Enum

from statemachine import StateMachine, State


class ServerStateTransition(Enum):
    slowdown = 1
    stop = 2
    go = 3


class TrafficLightMachine(StateMachine):
    state_start = State('Start State Machine', initial=True)
    green = State('Green')
    yellow = State('Yellow')
    red = State('Red')

    start = state_start.to(green)
    slowdown = green.to(yellow)
    stop = yellow.to(red)
    go = red.to(green)

    def __init__(self):
        super(TrafficLightMachine, self).__init__()
        self._lock = threading.Lock()
        self.curr_state = ...
        self.next_state = ...
        # thread_server_state_machine = threading.Thread(target=self.daemon_server_state_machine)  # , daemon=True)
        # thread_server_state_machine.start()

    def daemon_server_state_machine(self):
        self.start()
        while True:
            time.sleep(2)
            print(f'{self.curr_state} ... {self.next_state}')
            if self.curr_state == self.next_state:
                print(f'{self.curr_state} == {self.next_state}')
                continue
            with self._lock:
                self.curr_state = self.next_state
            match self.curr_state:
                case ServerStateTransition.slowdown:
                    self.slowdown()
                case ServerStateTransition.stop:
                    self.stop()
                case ServerStateTransition.go:
                    self.go()

    def on_enter_green(self):
        print(self.current_state)
        with self._lock:
            self.next_state = ServerStateTransition.slowdown

    def on_enter_yellow(self):
        print(self.current_state)
        with self._lock:
            self.next_state = ServerStateTransition.stop

    def on_enter_red(self):
        print(self.current_state)
        with self._lock:
            self.next_state = ServerStateTransition.go


if __name__ == '__main__':
    tlm = TrafficLightMachine()
    tlm.daemon_server_state_machine()
