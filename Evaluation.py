from pypokerengine.api.game import setup_config, start_poker
from RandomPokerPlayer import *
from FuzzyPokerPlayer import *
from HonestPokerPlayer import *
import numpy as np
import os
import sys
from pprint import pprint
import platform

if len(sys.argv) != 2:
    print("usage: Evaluation.py [number of iterations]")
else:

    num = int(sys.argv[1])
    wins = []
    amount = []

    for i in range(num):
        print(i,'/',num)
        config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
        config.register_player(name="Fuzzy", algorithm=FuzzyPokerPlayer())
        config.register_player(name="Honest", algorithm=HonestPokerPlayer())
        game_result = start_poker(config, verbose=0)
        players = game_result['players']
        if players[0]['stack'] > players[1]['stack']:
            wins.append(1)
            amount.append(players[0]['stack']-players[1]['stack'])
        else:
            wins.append(0)
            amount.append(0)
        # if platform.system() == 'Windows':
        #     os.system('cls')
        # if platform.system() == 'Linux':
        #    os.system('clear')

    wins = np.array(wins)
    amount = np.array(amount)

    print('Number of wins: ', wins.sum(), ' out of ', num)
    print('By an average of ', amount.sum()/num, ' points.')
