from pypokerengine.players import BasePokerPlayer
from pprint import pprint
from Calculations import Calculations as calc
from Fuzzy_system import run_fuzzy_system

class FuzzyPokerPlayer(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        call_action_info = valid_actions[1]
        me = round_state['seats'][round_state['next_player']]
        opponent = round_state['seats'][1-round_state['next_player']]
        aggro = calc.player_aggressiveness(round_state)[opponent['uuid']]
        tight = calc.player_tightness(round_state)[opponent['uuid']]
        money_opponent = calc.get_money_score(round_state)[opponent['uuid']]
        money_me = calc.get_money_score(round_state)[me['uuid']]
        winprob = calc.get_winprob(round_state, hole_card)
        print('sys out', run_fuzzy_system(tight, aggro, money_opponent, money_me, winprob))
        action, amount = call_action_info["action"], call_action_info["amount"]
        return action, amount   # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return FuzzyPokerPlayer()
