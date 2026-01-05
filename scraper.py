"""
Twitter/X scraper using Selenium
"""

import time
import random
import os
import re
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from logger import setup_logger
logger = setup_logger("scraper")

SEARCH_HASHTAGS = [
    "#nifty",
    "#nifty50",
    "#sensex",
    "#banknifty",
    "#finnifty",
    "#midcap",
    "#smallcap",
    "#sebi"
]
PROFILE_PATH = r"C:\temp\selenium_profile"


def init_driver():
    os.makedirs(PROFILE_PATH, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-data-dir={PROFILE_PATH}")

    driver = webdriver.Chrome(options=options)
    logger.info("Chrome driver started")
    return driver


def extract_metric(tweet, testid):
    els = tweet.find_elements(By.XPATH, f".//*[@data-testid='{testid}']")
    if not els:
        return 0

    label = els[0].get_attribute("aria-label") or ""
    match = re.search(r"\d+", label.replace(",", ""))
    return int(match.group()) if match else 0


def extract_tweet_data(tweet, idx):
    text_nodes = tweet.find_elements(By.XPATH, ".//div[@lang]")
    if not text_nodes:
        logger.debug(f"Article #{idx} skipped (no text)")
        return None

    content = text_nodes[0].text.strip()
    if not content:
        return None

    try:
        timestamp = tweet.find_element(By.TAG_NAME, "time").get_attribute("datetime")
    except:
        return None

    data = {
        "tweet_id": hash(content),
        "content": content,
        "timestamp": timestamp,
        "likes": extract_metric(tweet, "like"),
        "retweets": extract_metric(tweet, "retweet"),
        "replies": extract_metric(tweet, "reply"),
    }

    return data


def scrape_tweets(target_count):
    """
    Scrapes tweets until target_count is reached across all keywords
    """

    driver = init_driver()
    all_tweets = []
    seen_ids = set()

    for tag in SEARCH_HASHTAGS:
        if len(all_tweets) >= target_count:
            break

        logger.info(f"Searching keyword: {tag}")
        url = f"https://x.com/search?q={quote(tag)}&src=typed_query&f=live"
        driver.get(url)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//article//div[@lang]"))
        )

        # Pre-scroll to stabilize feed
        for _ in range(3):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(2)

        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(all_tweets) < target_count:
            articles = driver.find_elements(By.XPATH, "//article")

            for idx, article in enumerate(articles):
                data = extract_tweet_data(article, idx)
                if not data:
                    continue

                if data["tweet_id"] in seen_ids:
                    continue

                seen_ids.add(data["tweet_id"])
                all_tweets.append(data)

                logger.info(
                    f"TWEET #{len(all_tweets)} | ❤️ {data['likes']} "
                    f"🔁 {data['retweets']} 💬 {data['replies']}"
                )

                if len(all_tweets) >= target_count:
                    break

            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(random.uniform(2, 3))

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                logger.info(f"No more tweets loading for {tag}")
                break
            last_height = new_height

    driver.quit()
    logger.info(f"Scraping completed: {len(all_tweets)} tweets")
    return all_tweets
