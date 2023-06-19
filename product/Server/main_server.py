# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import logging
from product.Common.command import Command
from product.Common.commandType import CommandType as Ct
from product.Server.clientCommandIssuer import *
from product.Server.clientCommandReceiver import *
from product.Server.networkConnectionManager import *
from product.Server.questionManager import QuestionManager
from product.Server.serverStateMachine import ServerStateMachine
from product.Server.userManager import *
# from product.Server.gameKeeper import GameKeeper

logger = ...
HOST = ''
PORT = 13579


def init_logger():
    global logger
    logger = logging.getLogger('mainServerLogger')
    fmt = "[%(levelname)s][%(filename)s:%(funcName)s():%(lineno)s] %(message)s"
    logging.basicConfig(format=fmt)
    logger.setLevel(logging.DEBUG)


def main():
    init_logger()

    user_manager = UserManager(logger)
    server = NetworkConnectionManager((HOST, PORT), ClientCommandReceiver)
    # ip, port = server.server_address
    server.logger = logger
    server.user_manager = user_manager

    client_command_issuer = ClientCommandIssuer(logger, user_manager)
    server.client_command_issuer = client_command_issuer

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    question_manager = QuestionManager()

    try:
        # ##### Initial Test Code #####
        # timestamp = 0
        # while True:
        #     time.sleep(5)
        #     print(f'Server main loop...')
        #     cmd = Command(Ct.cmdQuestion, 'What grade will I get?', timestamp)
        #     timestamp += 1
        #     client_command_issuer.send_command(1337, cmd)

        # ##### Skeletal Demo Code #####
        # while user_manager.get_user(1337) is None or user_manager.get_user(1234) is None:
        #     time.sleep(2)
        #
        # gc = GameKeeper(user_manager, [user_manager.users[1337], user_manager.users[1234]], client_command_issuer,
        #                 question_manager.get_random_question_set())
        # gc.play_game()
        # while True:
        #     time.sleep(5)

        # ##### Minimal Demo Code #####
        ssm = ServerStateMachine(user_manager, client_command_issuer, question_manager)
        ssm.daemon_server_state_machine()
    except KeyboardInterrupt:
        print(f'Caught keyboard interrupt, exiting...')
    finally:
        user_manager.wipe_socket()
        server.shutdown()
        server.server_close()


main()
