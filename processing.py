# processing.py
"""
Text cleaning, normalization, deduplication
"""

import re
import hashlib
import pandas as pd

from logger import setup_logger
logger = setup_logger("scraper")


URL_REGEX = re.compile(r"http\S+")


def clean_text(text):
    text = text.lower()
    text = URL_REGEX.sub("", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def deduplicate(df):
    """
    Deduplicate using both tweet_id and content hash
    """
    df["content_hash"] = df["content"].apply(
        lambda x: hashlib.md5(x.encode("utf-8")).hexdigest()
    )
    return df.drop_duplicates(subset=["tweet_id", "content_hash"])


def process_tweets(raw_tweets):
    logger.info(f"Processing {len(raw_tweets)} raw tweets")

    df = pd.DataFrame(raw_tweets)
    df["content"] = df["content"].astype(str).apply(clean_text)

    before = len(df)
    df = deduplicate(df)
    after = len(df)

    logger.info(f"Deduplicated tweets: {before} → {after}")
    return df
