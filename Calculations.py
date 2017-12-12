from collections import Counter
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

class Calculations():

    def get_winprob(round_state, hole_card):
        return estimate_hole_card_win_rate(1000, 2, gen_cards(hole_card), gen_cards(round_state['community_card']))

    def get_money_score(round_state):
        scoredict = {}
        p1 = round_state['seats'][0]
        p2 = round_state['seats'][1]

        total = p1['stack'] + p2['stack']
        p1score = (1/total)*p1['stack']
        p2score = (1/total)*p2['stack']

        scoredict[p1['uuid']] = p1score
        scoredict[p2['uuid']] = p2score
        return scoredict

    def player_aggressiveness(round_state):
        """
            Returns a dictionary with the aggressiveness of each player
            per round
        """
        # initialise counters that will keep track of the amount of times a
        # player calls or bets
        p_calls = Counter()
        p_bets = Counter()
        # iterate over the action histories
        for key, value in round_state['action_histories'].items():
            # iterate over the actions of each player
            for player in value:
                uuid = player['uuid']
                # if a player calls add one to the counter
                if player['action'] == 'CALL':
                    p_calls[uuid] += 1
                # if a player raises add one to the counter
                if player['action'] == 'RAISE':
                    p_bets[uuid] += 1

        # make a list containg the player uuid's
        players = []
        for n in round_state['seats']:
            players.append(n['uuid'])

        # initialise a dictionary that will containg the player's aggressiveness
        aggress_dict = {}
        # calculate for each player the aggressiveness
        for player in players:
            # if the player hasn't bet, the aggressiveness is equal to 0
            if (player not in p_bets.keys()):
                aggress = 0
            # if the player hasn't called, the aggressiveness is equal to 1
            elif (player not in p_calls.keys()):
                aggress = 1
            # otherwise the aggressiveness is equal to the following formula
            else:
                aggress = p_bets[player] / (p_bets[player] + p_calls[player])
            aggress_dict[player] = aggress
        return aggress_dict


    def player_tightness(round_state):
        """
            Returns a dictionary with the tightness of each player
            per round
        """
        # initialise counters that will keep track of the amount of rounds and
        # times that a player zero bets
        p_zero_bet = Counter()
        n_rounds = 0
        # iterate over the action histories
        for key, value in round_state['action_histories'].items():
            # update the counter for the rounds
            n_rounds += 1
            # iterate over the actions of each player
            for player in value:
                uuid = player['uuid']
                # if a player zero raises add one to the counter
                if player['action'] == 'CALL':
                    if player['paid'] == 0:
                        p_zero_bet[uuid] += 1
                elif player['action'] == 'FOLD':
                    p_zero_bet[uuid] += 1

        # make a list containg the player uuid's
        players = []
        for n in round_state['seats']:
            players.append(n['uuid'])

        # initialise a dictionary that will containg the player's tightness
        tight_dict = {}
        # calculate for each player the tightness
        for player in players:
            tight = (1 + p_zero_bet[player]) / n_rounds
            tight_dict[player] = tight
        return tight_dict
