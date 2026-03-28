import pandas as pd

def compute_ic(score_df, future_returns):

    ic_values = []

    for date in future_returns.index:

        if date not in score_df.index:
            continue

        scores = score_df.loc[date]
        returns = future_returns.loc[date]

        if len(scores) < 2:
            continue

        ic = scores.corr(returns)

        ic_values.append(ic)

    ic_series = pd.Series(ic_values)

    return ic_series