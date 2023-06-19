import logging
import sys
from product.Client.clientStateMachine import ClientStateMachine
from product.Client.guiManager import GuiManager
from product.Client.networkConnectionManager import *
from product.Client.serverCommandIssuer import *
from product.Client.serverCommandReceiver import *

logger = ...


def init_logger():
    global logger
    logger = logging.getLogger('mainServerLogger')
    fmt = "[%(levelname)s][%(filename)s:%(funcName)s():%(lineno)s] %(message)s"
    logging.basicConfig(format=fmt)
    logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    init_logger()
    userID = 1337
    if len(sys.argv) > 1:
        print(f'Argument count : {len(sys.argv)}')
        print(f'Arg[1] = {sys.argv[1]}')
        userID = int(sys.argv[1])
    ncm = NetworkConnectionManager(user_id=userID)
    sci = ServerCommandIssuer(logger, ncm)
    scr = ServerCommandReceiver(logger, ncm, sci)
    scr.start()
    try:
        # ##### Skeletal Demo Code #####
        # if userID == 1234:
        #     sci.spam_server()
        # command = Command(Ct.cmdSpinWheel, userID, 0)
        # if sci.send_command(command) < 0:
        #     pass
        #
        # for turn in range(2):
        #     scr.status = 0
        #     while scr.status <= 0:
        #         time.sleep(1)
        #     qq = scr.question
        #     print(f'Question: {qq.question}')
        #     answer_input = input(f'Please choose an answer [A: {qq.option_A} B: {qq.option_B} C: {qq.option_C}]: ')
        #     # Temp: replying with answer, should be done in GUI with user input
        #     logger.info(f'Choosing answer {answer_input}')
        #     match answer_input:
        #         case 'A':
        #             answer = 0
        #         case 'B':
        #             answer = 1
        #         case 'C':
        #             answer = 2
        #         case _:
        #             answer = -1
        #     command = Command(Ct.cmdAnswer, answer, command.count)
        #     sci.send_command(command)
        #
        # sci.spam_server()

        csm = ClientStateMachine(userID, sci, scr)
        csm.start()
        gui_manager = GuiManager(csm)
        # sci.spam_server()
    except KeyboardInterrupt:
        print(f'Caught keyboard interrupt, exiting...')
    finally:
        ncm.disconnect_to_server()
        scr.join()
