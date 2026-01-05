# analysis.py
"""
Convert text → quantitative trading signal
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from logger import setup_logger
logger = setup_logger("scraper")

BULLISH_WORDS = ["buy", "breakout", "bullish", "long", "uptrend"]
BEARISH_WORDS = ["sell", "bearish", "short", "crash", "downtrend"]


def keyword_score(text):
    score = 0
    for w in BULLISH_WORDS:
        if w in text:
            score += 1
    for w in BEARISH_WORDS:
        if w in text:
            score -= 1
    return score


def engagement_weight(row):
    return np.log1p(row["likes"] + row["retweets"] + row["replies"])


def build_signal(df):
    logger.info("Building TF-IDF vectors")

    vectorizer = TfidfVectorizer(max_features=2000)
    tfidf = vectorizer.fit_transform(df["content"])

    logger.info("Calculating sentiment signal")

    df["keyword_score"] = df["content"].apply(keyword_score)
    df["engagement_weight"] = df.apply(engagement_weight, axis=1)
    df["signal"] = df["keyword_score"] * df["engagement_weight"]

    result = {
        "mean_signal": df["signal"].mean(),
        "confidence": df["signal"].std(),
        "tweet_count": len(df),
    }

    logger.info(f"Signal generated: {result}")
    return result
