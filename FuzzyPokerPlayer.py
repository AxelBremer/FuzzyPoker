from pypokerengine.players import BasePokerPlayer
from pprint import pprint
from Calculations import Calculations as calc
from Fuzzy_system import run_fuzzy_system
import math

def raise_amount(money_me, degree, action):
    if action == 'raise':
        return math.floor(money_me * degree)
    return 0

def unplayable(hole_card):
    suitedunplayable = [set(['Q', '7']),set(['Q', '6']),set(['Q', '5']),set(['Q', '4']),set(['Q', '3']),set(['Q', '2']),set(['J', '6']),set(['J', '5']),set(['J', '4']),set(['J', '3']),set(['J', '2']),set(['T', '5']),set(['T', '4']),set(['T', '3']),set(['T', '2']),set(['9', '5']),set(['9', '4']),set(['9', '3']),set(['9', '2']),set(['8', '5']),set(['8', '4']),set(['8', '3']),set(['8', '2']),set(['7', '4']),set(['7', '3']),set(['7', '2']),set(['6', '4']),set(['6', '3']),set(['6', '2']),set(['5', '3']),set(['5', '2']),set(['4', '3']),set(['4', '2']),set(['3', '2'])]
    unplayable = [set(['A', '6']),set(['A', '5']),set(['A', '4']),set(['A', '3']),set(['A', '2']),set(['K', '8']),set(['K', '7']),set(['K', '6']),set(['K', '5']),set(['K', '4']),set(['K', '3']),set(['K', '2']),set(['Q', '8']),set(['Q', '7']),set(['Q', '6']),set(['Q', '5']),set(['Q', '4']),set(['Q', '3']),set(['Q', '2']),set(['J', '7']),set(['J', '6']),set(['J', '5']),set(['J', '4']),set(['J', '3']),set(['J', '2']),set(['T', '7']),set(['T', '6']),set(['T', '5']),set(['T', '4']),set(['T', '3']),set(['T', '2']),set(['9', '6']),set(['9', '5']),set(['9', '4']),set(['9', '3']),set(['9', '2']),set(['8', '6']),set(['8', '5']),set(['8', '4']),set(['8', '3']),set(['8', '2']),set(['7', '6']),set(['7', '5']),set(['7', '4']),set(['7', '3']),set(['7', '2']),set(['6', '5']),set(['6', '4']),set(['6', '3']),set(['6', '2']),set(['5', '4']),set(['5', '3']),set(['5', '2']),set(['4', '3']),set(['4', '2']),set(['3', '2'])]
    if hole_card[0][0] == hole_card[1][0]:
        if set([hole_card[0][1], hole_card[1][1]]) in suitedunplayable:
            return True
    else:
        if set([hole_card[0][1], hole_card[1][1]]) in unplayable:
            return True
    return False

class FuzzyPokerPlayer(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        if unplayable(hole_card):
            print('action: fold unplayable hand')
            print('amount: 0')
            return 'fold', 0

        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        call_action_info = valid_actions[1]
        me = round_state['seats'][round_state['next_player']]
        opponent = round_state['seats'][1-round_state['next_player']]
        aggro = calc.player_aggressiveness(round_state)[opponent['uuid']]
        tight = calc.player_tightness(round_state)[opponent['uuid']]
        money_opponent = calc.get_money_score(round_state)[opponent['uuid']]
        money_me = calc.get_money_score(round_state)[me['uuid']]
        winprob = calc.get_winprob(round_state, hole_card)

        #action, amount = call_action_info["action"], call_action_info["amount"]
        (degree, action) = run_fuzzy_system(tight, aggro, money_opponent, money_me, winprob)
        amount = raise_amount(me['stack'], degree, action)
        # print('tight', tight)
        # print('aggro', aggro)
        # print('money_opponent', money_opponent)
        # print('money_me', money_me)
        # print('winprob', winprob)
        print('action: ', action)
        print('amount:', amount)
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
