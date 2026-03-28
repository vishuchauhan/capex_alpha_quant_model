import pandas as pd
from utils.regime_filter import regime_filter

def rolling_capex_backtest(price_data, capex_df, scoring_func, top_n=5):

    returns = price_data.pct_change().dropna()

    # Monthly rebalance
    dates = returns.resample("ME").first().index

    regime = regime_filter(price_data)

    portfolio_returns = []
    weights_history = {}

    for date in dates[:-1]:

        current_year = date.year

        score_df = scoring_func(capex_df, current_year)

        if score_df is None or score_df.empty:
            continue

        selected = score_df.sort_values("Capex Score", ascending=False).head(top_n)

        if selected.empty:
            continue

        scores = selected["Capex Score"].copy()
        scores = scores.replace([float("inf"), -float("inf")], 0).fillna(0)

        # SAFE WEIGHTS
        if scores.sum() == 0:
            weights = pd.Series(1 / len(scores), index=scores.index)
        else:
            weights = scores / scores.sum()

        # SAVE WEIGHTS (NEW FEATURE)
        weights_history[date] = weights

        next_period = returns.loc[date:date + pd.DateOffset(months=1)]

        if next_period.empty:
            continue

        common_cols = [col for col in selected.index if col in next_period.columns]

        if len(common_cols) == 0:
            continue

        weights = weights[common_cols]

        period_returns = next_period[common_cols].mul(weights, axis=1).sum(axis=1)

        # REGIME FILTER (SOFT)
        if date in regime.index and not regime.loc[date]:
            period_returns = period_returns * 0.7

        portfolio_returns.append(period_returns)

    if len(portfolio_returns) == 0:
        return pd.Series(dtype=float), pd.Series(dtype=float), {}

    portfolio_returns = pd.concat(portfolio_returns).sort_index()

    cumulative = (1 + portfolio_returns).cumprod()

    return cumulative, portfolio_returns, weights_history