from product.Common.userStatus import UserStatus as Us


class User:
    def __init__(self, user_id, sock=None, status=Us.usIdle, token=0, score1=0, score2=0):
        self.user_id = user_id
        self.sock = sock
        self.status = status
        self.token = token
        self.score1 = score1
        self.score2 = score2
        self.answer = ...
        self.category = -1
        self.use_token = None

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_socket(self):
        return self.sock

    def set_socket(self, sock):
        self.sock = sock

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_score(self, round_num=1):
        if round_num == 1:
            return self.score1
        else:
            return self.score2

    def set_score(self, score, round_num=1):
        if round_num == 1:
            self.score1 = score
        else:
            self.score2 = score

    def get_answer(self):
        return self.answer

    def set_answer(self, answer):
        self.answer = answer

    def clear_game_stat(self):
        self.score1 = 0
        self.score2 = 0
        self.token = 0
