import logging
from product.Server.user import User


class UserManager:
    def __init__(self, logger=None):
        self.users = {}
        if logger is None:
            self.logger = logging.getLogger('mainServerLogger')
            fmt = "[%(levelname)s][%(filename)s:%(funcName)s():%(lineno)s] %(message)s"
            logging.basicConfig(format=fmt)
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger = logger

    def add_user(self, user_id):
        if user_id in self.users:
            self.logger.debug(f'User {user_id} already exists.')
        else:
            self.users[user_id] = User(user_id)
        return self.users.get(user_id)

    def get_user(self, user_id):
        return self.users.get(user_id)

    def wipe_socket(self):
        for key in self.users:
            sock = self.users[key].get_socket()
            if sock is not None:
                sock.close()
                self.users[key].set_socket(None)


# Test Code
if __name__ == '__main__':
    um = UserManager()
    um.add_user(123)
    print(um.users)
    um.add_user(123)
    print(um.users)
    user = um.get_user(123)
    if user is not None:
        print(f'user id = {user.get_user_id()}')
    else:
        print(f'User does not exist.')
    user = um.get_user(1234)
    if user is not None:
        print(f'user id = {user.get_user_id()}')
    else:
        print(f'User does not exist.')
