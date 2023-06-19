class StatusPacket:
    def __init__(self, active_player_id, status_msg, status, question_num, round_num, remaining_spins, spin_result,
                 answer_result, pid1, score1a, score1b, token1, pid2, score2a, score2b, token2,
                 pid3=0, score3a=0, score3b=0, token3=0):
        self.active_player_id = active_player_id
        self.status_msg = status_msg
        self.status = status
        self.question_num = question_num
        self.round_num = round_num
        self.remaining_spins = remaining_spins
        self.spin_result = spin_result
        self.answer_result = answer_result
        self.player_id_1 = pid1
        self.score1a = score1a
        self.score1b = score1b
        self.token1 = token1
        self.player_id_2 = pid2
        self.score2a = score2a
        self.score2b = score2b
        self.token2 = token2
        self.player_id_3 = pid3
        self.score3a = score3a
        self.score3b = score3b
        self.token3 = token3
