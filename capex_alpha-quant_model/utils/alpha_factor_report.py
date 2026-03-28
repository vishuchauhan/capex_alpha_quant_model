import pandas as pd
import numpy as np

def factor_report(score_df):

    # =========================
    # SAFE HANDLING
    # =========================
    fin = score_df["Financial Contribution"].fillna(0)
    strat = score_df["Strategy Contribution"].fillna(0)
    nlp = score_df["NLP Contribution"].fillna(0)

    # =========================
    # 🔥 FIX: USE ABSOLUTE VALUES
    # =========================

    report = pd.DataFrame({
        "Factor": ["Financial", "Strategy", "NLP"],

        # This is the REAL alpha contribution
        "Avg Abs Contribution": [
            np.abs(fin).mean(),
            np.abs(strat).mean(),
            np.abs(nlp).mean()
        ],

        # Risk / variability of factor
        "Std Contribution": [
            fin.std(),
            strat.std(),
            nlp.std()
        ]
    })

    return report