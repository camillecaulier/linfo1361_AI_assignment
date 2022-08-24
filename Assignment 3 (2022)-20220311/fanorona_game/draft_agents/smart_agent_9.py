from core.player import Color
from fanorona.fanorona_player import FanoronaPlayer
from fanorona.fanorona_rules import FanoronaRules
from copy import deepcopy
import numpy as np
import time


class AI(FanoronaPlayer):
    name = "smart_agent_9"

    # transposition_table = {} #this will be the transposition table to relook up things
    def create_zorbit_keys(self):
        """
        we create a board where for each square we create a random 64 bit key for black and white
        this will allow us to create an almost unique board for each time we create one
        """
        # there should be 5 lines and the indexing should be accordning to the color
        zorbit_board = []
        rows = 5
        columns = 9
        for i in range(rows):
            temp = []
            for j in range(columns):
                zorbit_pair = [np.random, np.random]  # 1 will take the second element and -1 will take the first
                temp.append(zorbit_pair)
            zorbit_board.append(temp)
        return zorbit_board

    def __init__(self, color):
        super(AI, self).__init__(self.name, color)
        self.position = color.value  # the player who is playing currently
        # self.transposition_table = {}
        # self.keys_board = self.create_zorbit_keys() #i'm not sure if i'll use this or not
        # self.player_1_zorbit = np.random
        # self.player_2_zorbit = np.random
        self.total_nodes = 0
        self.game_depth = 3

    def play(self, state, remain_time):  # look at playgame line 220 fanorona gui
        print("")
        # print(state.)
        print(f"Player SMART AGENT 9 {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        # return iterative_deepening_min_max_search(state, self)
        return minimax_search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """

    def can_play_again(self, state):
        """
        function to tell if it will play again or not, we want to take into account max plays
        """
        return state.get_latest_player() == state.get_next_player()

    def successors(self, state,isMax):
        """
        FanoronaRules.get_player_actions(state, player)
        to get all the actions of a certain player. You need to yield each action together
        with the resulting state after the action is applied. This state is obtained by:
        FanoronaRules.act(state, action, player)
        Do not forget that you need to copy the state before you apply the action
        otherwise you will apply all actions to the input state. You can do this with the
        function copy.deepcopy(state).

        We are now adding ordering in order to place those that we think are more important
        ie those that are best with the eval function
        """
        # print("in actions")
        actions = FanoronaRules.get_player_actions(state, state.get_next_player())
        output = []

        for action in actions:
            state_copy = deepcopy(state)

            newstate, done = FanoronaRules.act(state_copy, action, state_copy.get_next_player())

            if newstate:
                output.append((action, newstate, self.amount_captured(newstate,isMax)))
                # output.append((action, newstate))

        output.sort(key=lambda output: output[2] , reverse=True)
        for tuple in range(len(output)):
            output[tuple] = (output[tuple][0], output[tuple][1])
        return output


    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """

    def cutoff(self, state, depth):
        """ function so that your agent greedily selects the best actions and will maximise the eval funciton"""

        if FanoronaRules.is_end_game(state):
            return True  # the game must end

        if depth == self.game_depth:
            return True

        return False

    def piece_advantage(self, state):
        """
        looks at the difference in piece according to the player, if you are in deficit or otherwise
        if you are in deficit it returns negative.
        """
        return state.score[self.color.value] - state.score[-self.color.value]
    def amount_captured(self, state,isMax):
        if isMax:
            return state.score[self.color.value]
        else:
            return state.score[-self.color.value]
    def evaluate(self, state):
        """"
        there are 22 total pieces in both sides
        """
        # score = state.score[self.color.value]  # number of pieces we have manged to take
        score = state.score[self.color.value] - state.score[-self.color.value]
        # print(score)
        return score


"""
MiniMax and AlphaBeta algorithms.
Adapted from:
    Author: Cyrille Dejemeppe <cyrille.dejemeppe@uclouvain.be>
    Copyright (C) 2014, Universite catholique de Louvain
    GNU General Public License <http://www.gnu.org/licenses/>
"""

inf = float("inf")

number_of_nodes = 0


def minimax_search(state, player, prune=True):
    """Perform a MiniMax/AlphaBeta search and return the best action.

    Arguments:
    state -- initial state
    player -- a concrete instance of class AI implementing an Alpha-Beta player
    prune -- whether to use AlphaBeta pruning

    """
    # print(state.get_json_state())
    global number_of_nodes
    number_of_nodes = 0

    def max_value(state, alpha, beta, depth):
        global number_of_nodes
        if player.cutoff(state, depth):
            return player.evaluate(state), None
        val = -inf
        action = None
        for a, s in player.successors(state,True):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = max_value(s, alpha, beta, depth)  # removed the  + 1 since the branchign is not that big
            else:  # next turn is for the other one
                v, _ = min_value(s, alpha, beta, depth + 1)
            if v > val:
                val = v
                action = a
                if prune:
                    if v >= beta:
                        return v, a
                    alpha = max(alpha, v)
        number_of_nodes += 1
        player.total_nodes += 1
        return val, action

    def min_value(state, alpha, beta, depth):  # simulation of the other player
        global number_of_nodes
        if player.cutoff(state, depth):
            return player.evaluate(state), None
        val = inf
        action = None
        for a, s in player.successors(state,False):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = min_value(s, alpha, beta, depth)  # removed the  +1
            else:  # next turn is for the other one
                v, _ = max_value(s, alpha, beta, depth + 1)
            if v < val:
                val = v
                action = a
                if prune:
                    if v <= alpha:
                        return v, a
                    beta = min(beta, v)
        number_of_nodes += 1
        player.total_nodes += 1
        return val, action

    # start_time = time.time()
    _, action = max_value(state, -inf, inf, 0)
    if int(state.score[player.color.value]) > 10:
        player.game_depth = player.game_depth + 1
    # print(time.time() - start_time)
    print("nodes for this search:" + str(number_of_nodes))
    print("total nodes:" + str(player.total_nodes))
    return action
