from scraper import scrape_tweets
from processing import process_tweets
from analysis import build_signal
from logger import setup_logger

logger = setup_logger("main")

MIN_TWEETS_REQUIRED = 100   # 👈 ONE place to control volume

def main():
    logger.info(f"Target tweets: {MIN_TWEETS_REQUIRED}")

    raw_tweets = scrape_tweets(target_count=MIN_TWEETS_REQUIRED)
    df = process_tweets(raw_tweets)

    signal = build_signal(df)

    logger.info("=== MARKET SENTIMENT ===")
    for k, v in signal.items():
        logger.info(f"{k}: {v}")

    df.to_parquet("tweets.parquet", index=False)
    logger.info("Saved tweets.parquet")

if __name__ == "__main__":
    main()
