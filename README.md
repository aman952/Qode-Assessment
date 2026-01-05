# Twitter/X Market Sentiment Scraper & Signal Engine
## User Guide & Logic Overview

---

## 1. What This System Does

This project collects real-time Indian stock market discussions from X (Twitter) and converts them into quantitative market sentiment signals that can be used for trading analysis or research.

In simple terms, the system:
- Opens X using your logged-in browser
- Searches for market-related hashtags (e.g. `#nifty50`, `#banknifty`)
- Scrolls and reads live tweets
- Extracts meaningful tweet data
- Cleans and deduplicates the data
- Converts text into numerical sentiment signals
- Saves structured data for further use

---

## 2. How to Run the Project (User Workflow)

### Step 1: Activate Environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Ensure X Login
- On first run, Chrome will open automatically
- Log in to X manually
- Close the browser
- From the next run onward, the login session is reused automatically

### Step 3: Run the Pipeline
```bash
python main.py
```

### You Will See:
- Live logs while tweets are being scraped
- Tweets printed as they are collected
- Final sentiment metrics in the console
- A `tweets.parquet` file generated

---

## 3. Scraping Logic (How Tweets Are Collected)

### Search Strategy
Each hashtag is searched individually using X’s live search.

Example:
```
https://x.com/search?q=%23nifty50&f=live
```

### Scrolling Logic
- The page is scrolled continuously
- New tweets are loaded dynamically
- Scrolling stops when no new content appears

### What Qualifies as a “Real Tweet”
A tweet is accepted only if:
- It contains actual tweet text (`div[@lang]`)
- It has a valid timestamp
- It is not a header, advertisement, or recommendation card

This filtering avoids noise and promotional content.

---

## 4. Tweet Extraction Logic

For each valid tweet, the following fields are captured:
- **Content** – actual tweet text
- **Timestamp** – UTC datetime from X
- **Likes**
- **Retweets**
- **Replies**
- **Tweet ID** – generated from content for stable deduplication

Tweets are printed live as they are saved so scraping progress is always visible.

---

## 5. Deduplication & Data Hygiene

To ensure clean and reliable data:
- Duplicate tweets are removed using:
  - Content hash
  - Tweet ID
- URLs are stripped
- Text is normalized (lowercase, spacing fixed)
- Unicode and mixed-language text is preserved safely

The final dataset contains unique, clean market discussions only.

---

## 6. Text → Signal Conversion Logic

### Keyword Sentiment Scoring
Each tweet is scanned for predefined keywords:
- **Bullish keywords** increase the score  
  *(e.g. buy, breakout, bullish, long)*
- **Bearish keywords** decrease the score  
  *(e.g. sell, bearish, crash, short)*

This produces a directional sentiment score.

### Engagement Weighting
Tweets with higher engagement carry more importance.

Engagement weight is computed as:
```
log(1 + likes + retweets + replies)
```

This prevents viral tweets from overpowering the signal while still rewarding relevance.

### Final Signal Calculation
```
Final Signal = Keyword Score × Engagement Weight
```

From all collected tweets:
- **Mean Signal** → overall market bias
- **Confidence** → signal consistency (volatility)
- **Tweet Count** → sample strength

---

## 7. Output Artifacts

After execution, the system generates:

### Console Output
- Live tweet logs
- Scraping progress
- Final sentiment summary

### Data Output
- `tweets.parquet`
  - Clean, deduplicated dataset
  - Ready for backtesting, dashboards, or ML pipelines

---

## 8. Why This Approach Works Well

- Uses real user sentiment instead of lagging indicators
- Avoids paid APIs
- Handles real-world web constraints
- Scales cleanly with increasing data volume
- Easy to extend with:
  - Additional keywords
  - Machine learning models
  - Sector-wise sentiment signals
  - Time-based aggregation

---

## Author
**Aman Priya**
