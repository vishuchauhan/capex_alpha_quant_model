import random

def nlp_agent(news_dict):

    nlp_scores = {}

    for ticker, headlines in news_dict.items():

        # =========================
        # BASE SENTIMENT LOGIC
        # =========================

        score = 0

        for headline in headlines:

            text = headline.lower()

            if "expansion" in text:
                score += 1

            if "capex" in text:
                score += 1

            if "plant" in text:
                score += 0.5

            if "debt" in text:
                score -= 0.5

        # =========================
        # 🔥 ADD VARIATION (VERY IMPORTANT)
        # =========================

        noise = random.uniform(-0.2, 0.2)

        score = score + noise

        # =========================
        # NORMALIZE
        # =========================

        score = max(score, 0)  # avoid negative NLP

        nlp_scores[ticker] = score

    return nlp_scores