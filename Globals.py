class Globals():
    def get_money_score(round_state):
        p1 = round_state['seats'][0]
        p2 = round_state['seats'][1]

        total = p1['stack'] + p2['stack']
        p1score = (1/total)*p1['stack']
        p2score = (1/total)*p2['stack']
        return p1score, p2score
