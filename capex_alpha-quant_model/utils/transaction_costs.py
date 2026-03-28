import pandas as pd

def apply_transaction_costs(weights_history, cost=0.001):
    """
    cost = 0.1% per trade
    """

    turnover_series = []

    prev_weights = None

    for date, weights in weights_history.items():

        if prev_weights is None:
            turnover = weights.abs().sum()
        else:
            turnover = (weights - prev_weights).abs().sum()

        turnover_series.append((date, turnover))
        prev_weights = weights

    turnover_df = pd.Series(
        dict(turnover_series)
    ).sort_index()

    # Transaction cost = turnover * cost
    cost_series = turnover_df * cost

    return turnover_df, cost_series