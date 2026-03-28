import pandas as pd
import matplotlib.pyplot as plt
import os

from data.capex_loader import load_capex_data
from data.market_data import load_market_data
from agents.financial_agent import financial_agent
from agents.nlp_agent import nlp_agent
from agents.industry_agent import industry_agent
from agents.strategy_agent import strategy_agent
from scoring.scoring_engine import compute_capex_scores
from backtest.capex_backtest import rolling_capex_backtest
from utils.risk_metrics import calculate_metrics
from utils.alpha_analysis import alpha_decomposition
from utils.advanced_metrics import advanced_metrics
from backtest.rolling_backtest import get_benchmark
from utils.transaction_costs import apply_transaction_costs

# =========================
# LOAD DATA
# =========================

capex_df = load_capex_data()

tickers = (
    capex_df["Ticker"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
    .tolist()
)

price_data = load_market_data(tickers, "2020-01-01", "2024-01-01")

# =========================
# NLP DATA
# =========================

news_dict = {
    ticker: [
        f"{ticker} expansion",
        f"{ticker} capex growth",
        f"{ticker} investment plan"
    ]
    for ticker in tickers
}

nlp_scores = nlp_agent(news_dict)

# =========================
# SCORING FUNCTION
# =========================

def scoring_func(capex_df, year):

    fin_scores, _ = financial_agent(capex_df, year)
    industry_ratio = industry_agent(fin_scores)
    strat_scores = strategy_agent(fin_scores, industry_ratio)

    score_df = compute_capex_scores(fin_scores, strat_scores, nlp_scores)

    return score_df

# =========================
# BACKTEST
# =========================

portfolio_cum, portfolio_returns, weights_history = rolling_capex_backtest(
    price_data,
    capex_df,
    scoring_func,
    top_n=5
)

# =========================
# BENCHMARK
# =========================

benchmark, _ = get_benchmark("2020-01-01", "2024-01-01")

portfolio_cum = portfolio_cum.squeeze()
benchmark = benchmark.squeeze().reindex(portfolio_cum.index)

# =========================
# TRANSACTION COSTS (NEW)
# =========================

turnover, cost_series = apply_transaction_costs(weights_history)

cost_series = cost_series.reindex(portfolio_returns.index).fillna(0)

portfolio_returns_net = portfolio_returns - cost_series
portfolio_cum_net = (1 + portfolio_returns_net).cumprod()

# =========================
# METRICS
# =========================

metrics = calculate_metrics(portfolio_returns)

print("\n=== METRICS ===")
for k, v in metrics.items():
    print(k, round(v, 3))

# =========================
# FINAL SCORES
# =========================

latest_year = capex_df["Year"].max()
final_scores_df = scoring_func(capex_df, latest_year)
final_scores_df = final_scores_df.sort_values("Capex Score", ascending=False)

# =========================
# ALPHA DECOMPOSITION
# =========================

alpha_df = alpha_decomposition(final_scores_df)

# =========================
# TOP PICKS
# =========================

top_picks = final_scores_df.head(5).copy()

def explain(row):
    reasons = []

    if row["Financial Score"] > 0:
        reasons.append("Strong capex growth")

    if row["Strategy Score"] > 0:
        reasons.append("Industry leader")

    if row["NLP Score"] > 0:
        reasons.append("Expansion narrative")

    return " | ".join(reasons)

top_picks["Reason"] = top_picks.apply(explain, axis=1)
top_picks["Recommendation"] = "BUY"

# =========================
# ADVANCED METRICS
# =========================

rolling_sharpe, drawdown_series = advanced_metrics(portfolio_returns)

# =========================
# IC (PROXY ADDITION)
# =========================

ic_series = portfolio_returns.rolling(20).mean()
avg_ic = ic_series.mean()

print("IC:", round(avg_ic, 3))

# =========================
# SAVE EXCEL
# =========================

os.makedirs("output", exist_ok=True)

file_path = "output/final_capex_results.xlsx"

if os.path.exists(file_path):
    os.remove(file_path)

with pd.ExcelWriter(file_path) as writer:

    pd.DataFrame({
        "Portfolio": portfolio_cum,
        "NIFTY": benchmark
    }).to_excel(writer, sheet_name="Performance")

    final_scores_df.to_excel(writer, sheet_name="Capex Scores")
    top_picks.to_excel(writer, sheet_name="Top Picks")
    alpha_df.to_excel(writer, sheet_name="Alpha Breakdown")

    final_scores_df[
        ["Financial Contribution", "Strategy Contribution", "NLP Contribution"]
    ].to_excel(writer, sheet_name="Score Contributions")

    rolling_sharpe.to_excel(writer, sheet_name="Rolling Sharpe")
    drawdown_series.to_excel(writer, sheet_name="Drawdown Curve")

    # NEW SHEETS
    turnover.to_excel(writer, sheet_name="Turnover")
    cost_series.to_excel(writer, sheet_name="Transaction Costs")
    portfolio_cum_net.to_excel(writer, sheet_name="Net Performance")
    ic_series.to_excel(writer, sheet_name="IC Series")

print("✅ ALL OUTPUTS SAVED")

# =========================
# PLOTS
# =========================

plt.figure(figsize=(10, 5))
plt.plot(portfolio_cum, label="Capex Strategy")
plt.plot(benchmark, label="NIFTY")
plt.legend()
plt.title("Dynamic Capex Strategy vs NIFTY")
plt.show()

plt.figure()
plt.plot(drawdown_series)
plt.title("Drawdown Curve")
plt.show()

plt.figure()
plt.plot(rolling_sharpe)
plt.title("Rolling Sharpe Ratio")
plt.show()

# NEW PLOTS

plt.figure()
plt.plot(turnover)
plt.title("Turnover")
plt.show()

plt.figure()
plt.plot(cost_series)
plt.title("Transaction Costs")
plt.show()

plt.figure()
plt.plot(portfolio_cum_net)
plt.title("Net Performance After Costs")
plt.show()

plt.figure()
plt.plot(ic_series)
plt.title("Information Coefficient (Proxy)")
plt.show()