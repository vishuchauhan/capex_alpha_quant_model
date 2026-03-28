import pandas as pd

def strategy_agent(financial_scores, industry_ratio):

    s = pd.Series(financial_scores)

    # 🔥 Leader threshold
    threshold = s.quantile(0.7)

    strategy_scores = {}

    for ticker, value in s.items():

        if value >= threshold:
            score = 3  # leader
        else:
            score = 1 + value  # follower

        if industry_ratio > 0.6:
            score += 0.5

        strategy_scores[ticker] = score

    return strategy_scores