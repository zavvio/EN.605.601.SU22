from product.Server.userManager import UserManager


class Scoreboard:

    def __init__(self, user_manager, players):
        self.user_manager = user_manager
        self.scoreDict = {}
        self.numOfPlayers = len(players)
        self.players = players
        # # Creates score dictionary info for a set number of Players and sets their scores to 0
        # for i in range(self.numOfPlayers):
        #     scores = {'Round Score': 0, 'Total Score': 0}
        #     self.scoreDict[players[i].get_user_id()] = scores

    # adds or subtracts points to round score
    def update_round_score(self, points, player_id, round_num=1):
        if round_num == 2:
            points *= 2
        curr_score = self.user_manager.get_user(player_id).get_score(round_num)
        new_score = curr_score + points
        print(f'User {player_id} has a round {round_num} score of {new_score}')
        self.user_manager.get_user(player_id).set_score(new_score, round_num)

    # # adds or subtracts points to overall score
    # def update_total_score(self, points, player_id):
    #     curr_score = self.scoreDict[player_id]['Total Score']
    #     new_score = curr_score + points
    #     self.scoreDict[player_id]['Total Score'] = new_score
    #     result = f'User {player_id} now has a total score of ' \
    #              + str(self.scoreDict[player_id]['Total Score'])
    #     print(result)
    #     return result

    # resets the score for the new round
    def reset_round_scores(self):
        # for i in range(self.numOfPlayers):
        #     self.scoreDict[list(self.user_manager.users)[i]]['Round Score'] = 0
        for player in self.players:
            player.set_score(0)

    # # helper function that resets total score
    # def reset_total_scores(self):
    #     for i in range(self.numOfPlayers):
    #         self.scoreDict[list(self.user_manager.users)[i]]['Total Score'] = 0

    # bankrupts a player
    def bankrupt(self, player_id, round_num=1):
        self.user_manager.get_user(player_id).set_score(0, round_num)
        print(f'User {player_id} has a round score of 0')

    # resets every player's round scores and overall scores to 0
    def reset_all(self):
        self.reset_round_scores()
        # self.reset_total_scores()

    # finds the winner and checks for ties
    def find_winner(self):
        winner = {}
        # for (key, value) in self.scoreDict.items():
        #     max_value = max(i['Total Score'] for i in self.scoreDict.values())
        #     for k in value:
        #         if value[k] == max_value:
        #             winner[key] = k
        # winner_list = list(winner.keys())
        # scores = {}
        # res = ''
        # for i in range(len(winner_list)):
        #     scores = self.scoreDict[winner_list[i]]['Total Score']
        winners = []
        max_score = -100000
        for player in self.players:
            s = player.get_score(1) + player.get_score(2)
            if s > max_score:
                max_score = s
                winners.clear()
                winners.append(player.get_user_id())
            elif s == max_score:
                winners.append(player.get_user_id())
        if len(winners) > 1:
            res = f'Users {", ".join(repr(e) for e in winners)} ' \
                  f'have tied with the same score of {max_score}'
            print(res)
            return res
        else:
            res = f'User {", ".join(repr(e) for e in winners)} ' \
                  f'is the winner with a score of {max_score}'
            print(res)
            return res


# Testing
if __name__ == '__main__':
    um = UserManager()
    um.add_user(123)
    um.add_user(321)
    score = Scoreboard(um)

    score.update_round_score(500, 123)
    score.update_round_score(500, 321)
    score.find_winner()
    score.reset_all()

    score.update_round_score(400, 123)
    score.update_round_score(500, 321)
    score.find_winner()
