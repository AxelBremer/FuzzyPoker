from pypokerengine.api.game import setup_config, start_poker
from RandomPokerPlayer import RandomPokerPlayer
from pprint import pprint

config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
config.register_player(name="p1", algorithm=RandomPokerPlayer())
config.register_player(name="p2", algorithm=RandomPokerPlayer())
game_result = start_poker(config, verbose=1)

pprint(game_result)
