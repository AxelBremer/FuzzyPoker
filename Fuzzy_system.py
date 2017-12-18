import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
from scipy import spatial
from operator import itemgetter

# Visualize these universes and membership functions
def visualize_memberships(X, x1mem, x2mem, x3mem, titles):
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

    ax0.plot(X[0], x1mem[0], 'b', linewidth=1.5, label='Low')
    ax0.plot(X[0], x1mem[1], 'g', linewidth=1.5, label='Medium')
    ax0.plot(X[0], x1mem[2], 'r', linewidth=1.5, label='High')
    ax0.set_title(titles[0])
    ax0.legend()

    ax1.plot(X[1], x2mem[0], 'b', linewidth=1.5, label='Low')
    ax1.plot(X[1], x2mem[1], 'g', linewidth=1.5, label='Medium')
    ax1.plot(X[1], x2mem[2], 'r', linewidth=1.5, label='High')
    ax1.set_title(titles[1])
    ax1.legend()

    ax2.plot(X[2], x3mem[0], 'b', linewidth=1.5, label='Low')
    ax2.plot(X[2], x3mem[1], 'g', linewidth=1.5, label='Medium')
    ax2.plot(X[2], x3mem[2], 'r', linewidth=1.5, label='High')
    ax2.set_title(titles[2])
    ax2.legend()

    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
    plt.tight_layout()

def visualize_result(X, mem3, risk0,  aggregated, result):

    activation = fuzz.interp_membership(X[2], aggregated, result)
    fig, ax0 = plt.subplots(figsize=(8, 3))
    ax0.plot(X[2], mem3[0], 'b', linewidth=0.5, linestyle='--', )
    ax0.plot(X[2], mem3[1], 'g', linewidth=0.5, linestyle='--')
    ax0.plot(X[2], mem3[2], 'r', linewidth=0.5, linestyle='--')
    ax0.fill_between(X[2], risk0, aggregated, facecolor='Orange', alpha=0.7)
    ax0.plot([result, result], [0, activation], 'k', linewidth=1.5, alpha=0.9)
    ax0.set_title('Aggregated membership and result (line)')

    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.show()

# Function to compute simple membership functions
def compute_memberships(X, set):
    memberships = [None] * len(X)
    for i in range(0, len(X)):
        low = fuzz.trimf(X[i], [set[0], set[0], set[1]])
        med =  fuzz.trimf(X[i], set)
        high =  fuzz.trimf(X[i], [set[1], set[2], set[2]])
        memberships[i] = [low, med, high]
    return memberships

# This function returns the appropriate rules to apply to the fuzzy problem
def rule_base(var1, var2, mem3, variable):
    defuzz_method = "mom"

    if variable == "risk":
        # if tightness low and agrresiveness high then risk aversion low
        rule1 = np.fmin(var1[0], var2[2])
        a1 = np.fmin(rule1, mem3[0])
        # if tightness medium or aggressiveness medium then risk aversion medium
        rule2 = np.fmax(var1[1], var2[1])
        a2= np.fmin(rule2, mem3[1])
        # if tightness high and aggressiveness low then risk aversion high
        rule3 = np.fmin(var1[2], var2[0])
        a3 = np.fmin(rule3, mem3[2])

        defuzz_method = "mom"

    if variable == "quality":
        # If risk aversion is low and money left is high then quality cards is low
        active_rule1 = np.fmin(var1[0] , var2[2])
        a1 = np.fmin(active_rule1, mem3[0])
        # if risk aversion is medium or money left is medium then quality of cards is medium
        active_rule2 = np.fmax(var1[1], var2[1])
        a2= np.fmin(active_rule2, mem3[1])
        # if risk aversion is high and money left is low then quality cards is high
        active_rule3 = np.fmax(var1[2], var2[0])
        a3 = np.fmin(active_rule3, mem3[2])

    if variable == "odds":
        # If probability hand is low or money left is low then odds player is low
        active_rule1 = np.fmin(var1[0] , var2[0])
        a1 = np.fmin(active_rule1, mem3[0])
        # if probability hand is medium then odds player is medium
        a2= np.fmax(var1[2], mem3[1])
        # if probability hand is high and money left is high then odds player is high
        active_rule3 = np.fmax(var1[2], var2[2])
        a3 = np.fmin(active_rule3, mem3[2])

        defuzz_method = "bisector"

    if variable == "strategy":
        # If odds player low then strategy fold
        a1 = np.fmin(var2[0], mem3[0])
        # if quality opponent low and odds player medium then strategy call
        a2= np.fmin(var2[1], mem3[1])
        # if quality opponent low and odds player high then strategy raise
        rule3= np.fmin(var1[0], var2[2])
        a3 = np.fmin(rule3, mem3[2])
        defuzz_method = "bisector"

    return a1, a2, a3, defuzz_method

# Fuzzy inference system
def fuzzy_inference(X, value1, value2, members, rules):
    mem1 = members[0]
    mem2 = members[1]
    mem3 = members[2]

    var1_low = fuzz.interp_membership(X[0], mem1[0], value1)
    var1_med = fuzz.interp_membership(X[0], mem1[1], value1)
    var1_high = fuzz.interp_membership(X[0], mem1[2], value1)
    var1 = [var1_low, var1_med, var1_high]

    var2_low = fuzz.interp_membership(X[1], mem2[0], value2)
    var2_med = fuzz.interp_membership(X[1], mem2[1], value2)
    var2_high = fuzz.interp_membership(X[1], mem2[2], value2)
    var2 = [var2_low, var2_med, var2_high]

    # Apply appropriate rule base
    activation_low, activation_med, activation_high, method= rule_base(var1, var2, mem3,rules)
    risk0 = np.zeros_like(X[0])

    # Aggregation of the three output memership functions
    aggregated = np.fmax(activation_low, np.fmax(activation_med, activation_high))

    # Defuzzify aggregation to crisp value
    result = fuzz.defuzz(X[2], aggregated, method)
    return result, risk0, aggregated

def fuzzy_inference_output(X, value1, value2, members, rules):
    mem1 = members[0]
    mem2 = members[1]
    mem3 = members[2]

    var1_low = fuzz.interp_membership(X[0], mem1[0], value1)
    var1_med = fuzz.interp_membership(X[0], mem1[1], value1)
    var1_high = fuzz.interp_membership(X[0], mem1[2], value1)
    var1 = [var1_low, var1_med, var1_high]

    var2_low = fuzz.interp_membership(X[1], mem2[0], value2)
    var2_med = fuzz.interp_membership(X[1], mem2[1], value2)
    var2_high = fuzz.interp_membership(X[1], mem2[2], value2)
    var2 = [var2_low, var2_med, var2_high]

    # Apply appropriate rule base
    activation_low, activation_med, activation_high, method= rule_base(var1, var2, mem3,rules)
    risk0 = np.zeros_like(X[0])

    # Aggregation of the three output memership functions
    aggregated = np.fmax(activation_low, np.fmax(activation_med, activation_high))

    # Calculate the similarity between the aggregated array and the
    # output membership function array
    fold_val = 1 - spatial.distance.cosine(aggregated, mem3[0])
    call_val = 1 - spatial.distance.cosine(aggregated, mem3[1])
    raise_val = 1 - spatial.distance.cosine(aggregated, mem3[2])

    # Define an action related to the cosine similarity
    actions = [(fold_val, 'FOLD'),(call_val, 'CALL'), (raise_val, 'RAISE')]

    # The result is the action related to the highest similarity
    result = max(actions,key=itemgetter(0))[1]

    return result, risk0, aggregated

def run_fuzzy_system(tightness, aggressiveness, money_opponent, money_player, probability_hand ):
    # Compute risk aversion opponent
    # Input: tightness and aggressiveness of the opponent
    # Output: risk aversive behavior of the opponent
    tight = np.arange(0, 1, 0.1)
    x_aggress = np.arange(0, 1, 0.1)
    x_risk_av  = np.arange(0, 1, 0.1)
    Risk = [tight, x_aggress, x_risk_av]
    risk_members = compute_memberships(Risk, [0, 0.5, 1])
    aversion, risk0, aggregated= fuzzy_inference(Risk, tightness, aggressiveness, risk_members, "risk")
    titles = ["Tightness opponent", "Aggressiveness opponent", "Risk aversive behavior"]
    # visualize_memberships(Risk, risk_members[0], risk_members[1], risk_members[2], titles)
    # visualize_result(Risk, risk_members[2], risk0, aggregated, aversion)
    # print("aversion", aversion)

    # Compute quality cards opponent
    # Input: risk aversive behavior and money left opponent
    # Output: estimation of the quality of the cards of opponent
    x_left_opponent = np.arange(0, 1, 0.1)
    x_quality = np.arange(0, 1, 0.1)
    Quality = [x_risk_av, x_left_opponent, x_quality ]
    quality_members = compute_memberships(Quality, [0, 0.5, 1])
    quality_cards_opponent, risk0, aggregated = fuzzy_inference(Quality, aversion, money_opponent, quality_members, "quality")
    titles = ["Risk aversion opponent", "Money left opponent ", "Quality cards opponent"]
    #visualize_memberships(Quality, quality_members[0], quality_members[1], quality_members[2], titles)
    #visualize_result(Quality, quality_members[2], risk0, aggregated, quality_cards_opponent)
    # print("quality", quality_cards_opponent)

    # Compute odds player
    # Input: probability hand of hand player and money left player
    # Ouput: estimation of how good the players chances are
    probability= np.arange(0, 1, 0.1)
    money_left_player = np.arange(0, 1, 0.1)
    player_odds = np.arange(0, 1, 0.1)
    Odds = [probability, money_left_player, player_odds ]
    odds_members = compute_memberships(Odds, [0, 0.5, 1])
    odds_player, risk0, aggregated = fuzzy_inference(Odds, probability_hand, money_player, odds_members, "odds")
    titles = ["Probability hand", "Money left player", "Odds player"]
    #visualize_memberships(Odds, odds_members[0], odds_members[1], odds_members[2], titles)
    #visualize_result(Odds, odds_members[2], risk0, aggregated, odds_player)
    # print("odds", odds_player)


    # Compute optimal strategy player
    # Input: quality cards opponent and odds player
    # Ouput: indication of optimal strategy for player
    strategy_optimal = np.arange(0, 1, 0.1)
    Strategy = [x_quality, player_odds, strategy_optimal ]
    strategy_members = compute_memberships(Strategy, [0, 0.5, 1])
    optimal, risk0, aggregated = fuzzy_inference_output(Strategy, quality_cards_opponent, odds_player, strategy_members, "strategy")
    titles = ["Quality cards opponent", "Odds player", "Strategy"]
    #visualize_memberships(Odds, odds_members[0], odds_members[1], odds_members[2], titles)
    #visualize_result(Odds, odds_members[2], risk0, aggregated, optimal)
    # print("optimal  crisp", optimal)
    return optimal

# UNCOMMENT FOR TESTING
# tight = [0.1, 1, 0.5, 0]
# aggressive = [0.8, 0.1, 0.5, 0]
# money_opponent = [0.7, 0.2, 0.4, 0]
# money_player= [0.4, 0.8, 0.6, 0]
# probability = [0.9, 0.3, 0.5, 0]
# for i in range(len(tight)):
#     optimal = run_fuzzy_system(tight[i], aggressive[i], money_opponent[i], money_player[i], probability[i])
