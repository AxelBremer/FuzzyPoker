from pypokerengine.players import BasePokerPlayer
from pprint import pprint
import random

class RandomPokerPlayer(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        num_actions = len(valid_actions)
        action_info = valid_actions[random.randint(0,num_actions-1)]
        pprint(valid_actions)
        pprint('Chosen action:')
        pprint(action_info)
        pprint(hole_card)
        pprint(round_state)
        action = action_info['action']
        if type(action_info['amount']) == int:
            amount = action_info['amount']
        else:
            amount = random.randint(action_info['amount']['min'], action_info['amount']['max'])
        input('...')
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
