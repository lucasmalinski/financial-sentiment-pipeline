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
        full_df = pd.concat([old_df, new_df], ignore_index=True)
        full_df.drop_duplicates(subset='headline', inplace=True)
    else:
        full_df = new_df

    # Step 3: Download BTC data
    btc_data = yf.download(TICKER, period=DATA_PERIOD, interval="1h")
    btc_data.index = btc_data.index.tz_localize(None)

    # Step 4: Add BTC prices if missing
    if 'btc_price' not in full_df.columns:
        full_df['btc_price'] = None

    full_df['btc_price'] = full_df.apply(
        lambda row: row['btc_price'] if pd.notna(row['btc_price']) else get_btc_price_at(pd.to_datetime(row['parsed_timestamp']), btc_data),
        axis=1
    )

    # Step 5: Save results
    full_df.to_csv(OUTPUT_CSV_FILE, index=False)
    print(f"\n✅ Saved {len(full_df)} headlines to '{OUTPUT_CSV_FILE}'")

if __name__ == "__main__":
    main()
# --- End of parse_and_combine.py ---           