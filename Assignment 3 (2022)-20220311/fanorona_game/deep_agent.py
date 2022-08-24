from core.player import Color
from fanorona.fanorona_player import FanoronaPlayer
from fanorona.fanorona_rules import FanoronaRules
from copy import deepcopy


class AI(FanoronaPlayer):
    name = "deep_agent"

    def __init__(self, color):
        super(AI, self).__init__(self.name, color)
        self.position = color.value  #the player who is playing currently
        self.total_nodes = 0

    def play(self, state, remain_time): #look at playgame line 220 fanorona gui
        print("")
        print(f"Player BASIC AGENT {self.position} is playing.")
        print("time remain is ", remain_time, " seconds")
        return minimax_search(state, self)

    """
    The successors function must return (or yield) a list of
    pairs (a, s) in which a is the action played to reach the
    state s.
    """

    def successors(self, state):
        """
        FanoronaRules.get_player_actions(state, player)
        to get all the actions of a certain player. You need to yield each action together
        with the resulting state after the action is applied. This state is obtained by:
        FanoronaRules.act(state, action, player)
        Do not forget that you need to copy the state before you apply the action
        otherwise you will apply all actions to the input state. You can do this with the
        function copy.deepcopy(state).
        """
        # print("in actions")
        actions = FanoronaRules.get_player_actions(state, state.get_next_player())
        output = []
        # print(actions)
        for action in actions:
            state_copy = deepcopy(state)
            # print("fuck")
            # newstate, done = FanoronaRules.act(state_copy, action, state_copy.get_next_player())
            newstate, done = FanoronaRules.act(state_copy, action, state_copy.get_next_player())

            # print("yolo")
            # print(newstate)
            if newstate:
                output.append((action, newstate))
        return output

    """
    The cutoff function returns true if the alpha-beta/minimax
    search has to stop and false otherwise.
    """

    def cutoff(self, state, depth):
        """ function so that your agent greedily selects the best actions and will maximise the eval funciton"""
        # print("in cutoff\n")
        # print(depth)
        # print("hello")
        # for when the game is over
        if FanoronaRules.is_end_game(state):
            return True  # the game must end
        if depth == 8: #or 6
            return True

        return False


    """
    The evaluate function must return an integer value
    representing the utility function of the board. this must be done with respect to your player
    (1 for the green player, −1 for white player)
    """

    def evaluate(self, state):
        """"
        there are 22 total pieces in both sides
        """
        # print("in evaluate")
        score = state.score[self.color.value]
        # score = state.captured
        # print(score)
        # print(state.board)
        return score
        # pass  # TODO replace by your code


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
        for a, s in player.successors(state):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = max_value(s, alpha, beta, depth + 1)
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

    def min_value(state, alpha, beta, depth): #simulation of the other player
        global number_of_nodes
        if player.cutoff(state, depth):
            return player.evaluate(state), None
        val = inf
        action = None
        for a, s in player.successors(state):
            if s.get_latest_player() == s.get_next_player():  # next turn is for the same player
                v, _ = min_value(s, alpha, beta, depth + 1)
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

    _, action = max_value(state, -inf, inf, 0)
    print("nodes for this search:" + str(number_of_nodes))
    print("total nodes:" + str(player.total_nodes))
    return action
