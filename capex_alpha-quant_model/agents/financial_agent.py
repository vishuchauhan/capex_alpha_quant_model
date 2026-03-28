import pandas as pd

def financial_agent(capex_df, year):

    df = capex_df[capex_df["Year"] == year]

    financial_scores = {}
    components = {}

    for _, row in df.iterrows():

        ticker = row["Ticker"]

        cwip = row.get("CWIP", 0)
        assets = row.get("TotalAssets", 1)
        debt = row.get("Debt", 0)

        # 🔥 SAFE HANDLING
        if pd.isna(cwip): cwip = 0
        if pd.isna(assets) or assets == 0: assets = 1
        if pd.isna(debt): debt = 0

        # =========================
        # 🔥 QUANT CAPEX SIGNAL
        # =========================

        # 1. Capex intensity
        capex_ratio = cwip / assets

        # 2. Debt penalty (game theory: leveraged firms risky)
        debt_ratio = debt / assets

        # 3. Final financial signal
        score = capex_ratio - 0.5 * debt_ratio

        financial_scores[ticker] = score

        # Store components (for explainability later if needed)
        components[ticker] = {
            "capex_ratio": capex_ratio,
            "debt_ratio": debt_ratio
        }

    # =========================
    # 🔥 CROSS-SECTIONAL RANK (VERY IMPORTANT)
    # =========================

    s = pd.Series(financial_scores)

    if s.std() != 0:
        ranked = s.rank(pct=True)
    else:
        ranked = pd.Series(0.5, index=s.index)

    financial_scores = ranked.to_dict()

    return financial_scores, components