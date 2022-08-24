"""
Created on 30 oct. 10:37 2020

@author: HaroldKS
"""
import sys
import ctypes
import argparse
from PyQt5.QtWidgets import *
from core import Color
from gui import FanoronaGUI


if __name__ == '__main__':

    app_id = 'myfi.maic.yote.2.0'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except AttributeError:
        pass
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', help='total number of seconds credited to each player')
    parser.add_argument('-ai0', help='path to the ai that will play as player 0')
    parser.add_argument('-ai1', help='path to the ai that will play as player 1')
    parser.add_argument('-s', help='time to show the board')
    args = parser.parse_args()

    # set the time to play
    allowed_time = float(args.t) if args.t is not None else 5.0
    sleep_time = float(args.s) if args.s is not None else 0.

    player_type = ['human', 'human']
    player_type[0] = args.ai0 if args.ai0 != None else 'human'
    print(player_type[0])
    player_type[1] = args.ai1 if args.ai1 != None else 'human'
    for i in range(2):
        if player_type[i].endswith('.py'):
            player_type[i] = player_type[i][:-3]
    agents = {}

    # load the agents
    k = -1
    for i in range(2):
        #if it is a bot we create the agent
        if player_type[i] != 'human':
            j = player_type[i].rfind('/')
            # extract the dir from the agent
            dir = player_type[i][:j]
            # add the dir to the system path
            sys.path.append(dir)
            # extract the agent filename
            file = player_type[i][j + 1:]
            # create the agent instance
            agents[k] = getattr(__import__(file), 'AI')(Color(k))
            # print(agents[k].state)
            k *= -1
        # if player_type[i] == 'human':
        #     path_temp = 'fanorona/fanorona_player.py'
        #     # extract the dir from the agent
        #     dir = path_temp
        #     # add the dir to the system path
        #     sys.path.append(dir)
        #     # # extract the agent filename
        #     # file = player_type[i][j + 1:]
        #     # create the agent instance
        #     file = dir
        #     agents[k] = getattr(__import__(file), 'FanoronaPlayer')("hi",Color(k))
        #     # print(agents[k].state)
        #     k *= -1
        #
        #     agents[k] = getattr(__import__("fanorona_player.py"), 'FanoronaPlayer')("human",Color(k))
    if None in agents:
        raise Exception('Problems in  AI players instances. \n'
                        'Usage:\n'
                        '-t allowed time for each ai \n'
                        '\t total number of seconds credited to each player \n'
                        '-ai0 ai0_file.py \n'
                        '\t path to the ai that will play as player 0 \n'
                        '-ai1 ai1_file.py\n'
                        '\t path to the ai that will play as player 1 \n'
                        '-s sleep time \n'
                        '\t time(in second) to show the board(or move)')

    #we launch the game with the agents
    game = FanoronaGUI(app, (5, 9), agents, sleep_time=sleep_time, allowed_time=allowed_time)
    game.show()
    sys.exit(app.exec_())
