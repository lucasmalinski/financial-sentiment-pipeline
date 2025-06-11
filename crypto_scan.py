import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import os

# --- Configuration ---
TICKER = "BTC-USD"
DATA_PERIOD = "3mo"
OUTPUT_CSV_FILE = "financial_data_v1.0_debug.csv"
YAHOO_URL = "https://finance.yahoo.com/topic/crypto/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# === HTML Fetching ===
def fetch_html():
    print("\n📡 Fetching news headlines from Yahoo Finance...")
    response = requests.get(YAHOO_URL, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch HTML content. Status code: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

# === Timestamp Conversion ===
def convert_to_timestamp(time_str):
    now = datetime.now()
    time_str = time_str.lower()

    if "minute" in time_str:
        minutes = int(re.search(r'\d+', time_str).group())
        return now - timedelta(minutes=minutes)
    elif "hour" in time_str:
        hours = int(re.search(r'\d+', time_str).group())
        return now - timedelta(hours=hours)
    elif "yesterday" in time_str:
        return now - timedelta(days=1)
    else:
        return pd.NaT

# === BTC Price Lookup ===
def get_btc_price_at(timestamp, btc_data):
    if pd.isna(timestamp):
        return None
    closest_times = btc_data.index[btc_data.index <= timestamp]
    if not closest_times.empty:
        closest_time = closest_times[-1]
        return btc_data.loc[closest_time]["Close"]
    return None

# === News Parsing ===
def parse_news(soup):
    h3_tags = soup.find_all('h3', class_='clamp yf-1jsv3x8')
    timestamp_tags = soup.find_all('div', class_="publishing yf-1weyqlp")

    news = {}
    for i, tag in enumerate(h3_tags):
        headline = tag.text.strip().replace('"', '')
        if headline not in news and i < len(timestamp_tags):
            time_info = timestamp_tags[i].contents[2].text.strip()
            news[headline] = time_info

    df = pd.DataFrame(news.items(), columns=['headline', 'timestamp'])
    df['parsed_timestamp'] = df['timestamp'].apply(convert_to_timestamp)
    return df

# === Main Workflow ===
def main():
    # Step 1: Fetch and parse HTML
    soup = fetch_html()
    new_df = parse_news(soup)

    # Step 2: Load previous data if any
    if os.path.exists(OUTPUT_CSV_FILE):
        old_df = pd.read_csv(OUTPUT_CSV_FILE)
        # Identify new headlines only
        new_headlines = ~new_df['headline'].isin(old_df['headline'])
        only_new_df = new_df[new_headlines].copy()
        # Step 3: Download BTC data only if needed
        if not only_new_df.empty:
            btc_data = yf.download(TICKER, period=DATA_PERIOD, interval="1h")
            btc_data.index = btc_data.index.tz_localize(None)
            only_new_df['btc_price'] = only_new_df['parsed_timestamp'].apply(
                lambda ts: get_btc_price_at(pd.to_datetime(ts), btc_data)
            )
        # Combine, keeping old rows as-is
        full_df = pd.concat([only_new_df, old_df], ignore_index=True)
        # Drop duplicates, keeping the first (which is the new one if duplicated)
        full_df.drop_duplicates(subset='headline', keep='first', inplace=True)
    else:
        btc_data = yf.download(TICKER, period=DATA_PERIOD, interval="1h")
        btc_data.index = btc_data.index.tz_localize(None)
        new_df['btc_price'] = new_df['parsed_timestamp'].apply(
            lambda ts: get_btc_price_at(pd.to_datetime(ts), btc_data)
        )
        full_df = new_df

    # Sort so latest news is at index 0
    full_df.sort_values('parsed_timestamp', ascending=False, inplace=True, ignore_index=True)

    # Step 5: Save results
    full_df.to_csv(OUTPUT_CSV_FILE, index=False)
    print(f"\n✅ Saved {len(full_df)} headlines to '{OUTPUT_CSV_FILE}'")

if __name__ == "__main__":
    main()
# --- End of parse_and_combine.py ---