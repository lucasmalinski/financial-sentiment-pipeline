import yfinance as yf
import pandas as pd 

# Define the ticker symbol for Bitcoin-USD
ticker_symbol = "BTC-USD"

# Define the period for data fetching
data_period = "3mo"

stock_data = yf.download(ticker_symbol, period=data_period)

# Display the first row's of the dataframe
print("Successfully fetched BTC data:")
print(stock_data.head())

# Display the last row's of the dataframe
print("Successfully fetched BTC data:")
print(stock_data.tail())

import requests
from bs4 import BeautifulSoup

# ---- TARGET: YAHOO FINANCE NEWS ---
# Define the URL for the news source and headers for the request
news_url = "https://finance.yahoo.com/topic/crypto/" # More relevant to BTC!
# It's a best practice to set a User-Agent to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("\nFetching news headlines from Yahoo Finance...")

# Get the webpage's HTML content
response = requests.get(news_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the headline elements.
# On Yahoo Finance, headlines are typically in <h3> tags inside a link.
headlines = soup.find_all('h3')

# Print the first 5 headlines to verify
print("Successfully scraped headlines:")
scraped_headlines = []
for headline in headlines:
    # Yahoo includes non-headline 'h3's, so we filter by length.
    if len(headline.text) > 20: # A simple, working filter for yahoo headlines
        scraped_headlines.append(headline.text)

# Print the first 5 valid headlines found
for index, headline_text in enumerate(scraped_headlines[:10]):
    print(f"{index + 1}: {headline_text}")


