from pypokerengine.api.game import setup_config, start_poker
from RandomPokerPlayer import *
from FuzzyPokerPlayer import *
from pprint import pprint

config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
config.register_player(name="fuzzy1", algorithm=FuzzyPokerPlayer())
config.register_player(name="fuzzy2", algorithm=FuzzyPokerPlayer())
game_result = start_poker(config, verbose=1)

pprint(game_result)
