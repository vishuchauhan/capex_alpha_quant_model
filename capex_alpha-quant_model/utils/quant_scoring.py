import pandas as pd
import numpy as np

def zscore(series):
    if series.std() == 0:
        return pd.Series(0, index=series.index)
    return (series - series.mean()) / series.std()

def quant_score_transform(fin_scores, strat_scores, nlp_scores):

    df = pd.DataFrame({
        "Financial": pd.Series(fin_scores),
        "Strategy": pd.Series(strat_scores),
        "NLP": pd.Series(nlp_scores)
    }).fillna(0)

    # 🔥 Z-SCORE NORMALIZATION (CROSS-SECTIONAL)
    df["Financial_z"] = zscore(df["Financial"])
    df["Strategy_z"] = zscore(df["Strategy"])
    df["NLP_z"] = zscore(df["NLP"])

    return df