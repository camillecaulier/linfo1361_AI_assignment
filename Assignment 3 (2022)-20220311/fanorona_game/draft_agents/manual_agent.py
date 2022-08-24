from fanorona.fanorona_player import FanoronaPlayer
from fanorona.fanorona_rules import FanoronaRules
from fanorona.fanorona_action import FanoronaAction
from fanorona.fanorona_action import FanoronaActionType
from typing import *

class AI(FanoronaPlayer):

    name = "Manual Agent"

    def __init__(self, color):
        super(AI, self).__init__(self.name, color)
        self.position = color.value
        self.play_number = 0

    def play(self, state, remain_time):
        player = self.position
        actions: List[FanoronaAction] = FanoronaRules.get_player_actions(state, player)
        print("Available actions for play №" + str(self.play_number))
        for i, action in enumerate(actions):
            print(f"({i}) {[action.action, action.win_by]};")
        self.play_number += 1
        chosen_move: str = input()
        return actions[int(chosen_move)]