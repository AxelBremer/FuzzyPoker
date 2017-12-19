from pypokerengine.api.game import setup_config, start_poker
from RandomPokerPlayer import *
from FuzzyPokerPlayer import *
from pprint import pprint

config = setup_config(max_round=25, initial_stack=100, small_blind_amount=5)
config.register_player(name="Fuzzy", algorithm=FuzzyPokerPlayer())
config.register_player(name="Random", algorithm=RandomPokerPlayer())
game_result = start_poker(config, verbose=0)

pprint(game_result)
