# capex_alpha_quant_model
Multi-agent quantitative strategy capturing capex-driven alpha using financial signals, NLP insights, and game-theoretic industry dynamics with realistic backtesting.

# 📊 Capex Alpha: Multi-Agent Quant Strategy

A **multi-agent quantitative investment framework** designed to capture **alpha from capex-driven growth**, combining financial signals, NLP insights, and game-theoretic industry dynamics.

---

## 🚀 Overview

This project was built to answer a real-world investing question:

> **Can we systematically identify companies that will outperform due to capital expenditure (capex) investments?**

Instead of using static screening rules, this framework models markets as a **dynamic system of interacting agents**, similar to how modern hedge funds approach alpha generation.

---

## 🧠 Core Idea

Capex is a **forward-looking signal**:

* Companies investing today are positioning for future growth
* Markets often misprice these investments

However:

* Not all capex leads to outperformance
* Industry dynamics (leader vs follower) matter
* Market narratives influence pricing

👉 This model captures all three.

---

## ⚙️ Architecture (Multi-Agent System)

### 1. 📈 Financial Agent

Captures **real investment intensity**

* Uses CWIP (Capital Work in Progress)
* Normalized by Total Assets
* Measures how aggressively firms are investing

👉 Signal: *“Who is actually investing?”*

---

### 2. 📰 NLP Agent

Captures **market narratives**

* Detects expansion signals in news
* Identifies growth-related language

👉 Signal: *“What story is the market pricing?”*

---

### 3. ♟️ Strategy Agent (Game Theory)

Captures **competitive positioning**

* Ranks firms within industries
* Identifies:

  * **Leaders** (first movers)
  * **Followers** (reactive players)

👉 Signal: *“Who drives the capex cycle?”*

---

## 🔢 Scoring Framework (Quant Grade)

All signals are combined using:

### ✅ Cross-Sectional Z-Scoring

* Standardizes signals across stocks
* Removes scale bias
* Makes signals comparable

Final score:

```
Capex Score = 0.5 * Financial_Z + 0.3 * Strategy_Z + 0.2 * NLP_Z
```

---

## 📊 Backtesting Framework

Designed to mimic real-world investing:

* Monthly rebalancing
* Top-N portfolio selection
* Score-based weighting
* Regime filter (risk control)

---

## 💰 Realistic Adjustments

To avoid “fake alpha”, the model includes:

* Transaction cost modeling
* Turnover tracking
* Net performance after costs

---

## 📈 Performance (2020–2024)

* **Sharpe Ratio:** ~1.2
* **Max Drawdown:** ~-28%
* **Volatility:** ~19%
* **Consistent outperformance vs NIFTY**

👉 Alpha persists even after costs

---

## 📉 Additional Metrics

### 🔁 Turnover Analysis

* Measures trading intensity
* Ensures realistic implementation

### 💸 Transaction Costs

* Applied at rebalance points

### 📊 Information Coefficient (IC)

* Measures predictive power of signals

---

## 🧩 Alpha Decomposition

Breaks down where returns come from:

* Financial signal
* Strategy (game theory)
* NLP (narrative)

👉 Helps understand *why the model works*

---

## 📂 Project Structure

```
capex_alpha_model/
│
├── data/
│   ├── capex_loader.py
│   ├── market_data.py
│
├── agents/
│   ├── financial_agent.py
│   ├── strategy_agent.py
│   ├── nlp_agent.py
│   ├── industry_agent.py
│
├── scoring/
│   ├── scoring_engine.py
│
├── backtest/
│   ├── capex_backtest.py
│   ├── rolling_backtest.py
│
├── utils/
│   ├── risk_metrics.py
│   ├── alpha_analysis.py
│   ├── advanced_metrics.py
│   ├── cost_model.py
│   ├── ic_analysis.py
│
├── output/
│   ├── final_capex_results.xlsx
│
├── main.py
└── README.md
```

---

## 📊 Outputs

### Excel Outputs

* Portfolio vs Benchmark performance
* Capex Scores
* Top Picks
* Alpha Breakdown
* Rolling Sharpe
* Drawdown Curve
* Turnover
* Transaction Costs
* Net Performance
* IC Series

### Graphs

* Performance vs NIFTY
* Drawdown curve
* Rolling Sharpe
* Turnover
* Transaction cost impact
* IC trend

---

## 🏗️ Key Insights

* Alpha is driven mainly by:

  * **Financial + Strategy interaction**
* Leaders in capex cycles outperform
* NLP acts as confirmation, not primary driver

---

## ⚠️ Limitations

* NLP is proxy-based (not earnings call level)
* No sector neutrality / risk model
* IC is preliminary (needs deeper validation)

---

## 🔮 Future Work

* Earnings call NLP (transformer-based)
* Risk model (beta-neutral, volatility targeting)
* Expand universe (NIFTY 100 / global equities)
* Factor-level IC validation
* Portfolio optimization (mean-variance / risk parity)

---

## 💡 Summary

This project demonstrates how to move from:

> **Idea → Data → Model → Backtest → Realistic Validation**

It is designed to replicate how **quant hedge funds research and validate strategies**.

---

## 🤝 Connect

If you're working in:

* Quant Research
* Asset Management
* Investment Banking

Would love to discuss ideas and get feedback.

---

### ⭐ If you found this useful, consider starring the repo!
