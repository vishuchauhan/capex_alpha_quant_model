import pandas as pd
import numpy as np

def zscore(series):
    if series.std() == 0:
        return pd.Series(0, index=series.index)
    return (series - series.mean()) / series.std()

def compute_capex_scores(fin_scores, strat_scores, nlp_scores):

    df = pd.DataFrame({
        "Financial": pd.Series(fin_scores),
        "Strategy": pd.Series(strat_scores),
        "NLP": pd.Series(nlp_scores)
    }).fillna(0)

    # 🔥 Z-SCORE NORMALIZATION
    df["Financial_z"] = zscore(df["Financial"])
    df["Strategy_z"] = zscore(df["Strategy"])
    df["NLP_z"] = zscore(df["NLP"])

    records = []

    for ticker in df.index:

        fin = df.loc[ticker, "Financial_z"]
        strat = df.loc[ticker, "Strategy_z"]
        nlp = df.loc[ticker, "NLP_z"]

        final_score = (
            0.5 * fin +
            0.3 * strat +
            0.2 * nlp
        )

        records.append({
            "Ticker": ticker,

            "Financial Score": fin_scores.get(ticker, 0),
            "Strategy Score": strat_scores.get(ticker, 0),
            "NLP Score": nlp_scores.get(ticker, 0),

            "Financial Z": fin,
            "Strategy Z": strat,
            "NLP Z": nlp,

            "Capex Score": final_score,

            "Financial Contribution": 0.5 * fin,
            "Strategy Contribution": 0.3 * strat,
            "NLP Contribution": 0.2 * nlp
        })

    return pd.DataFrame(records).set_index("Ticker")