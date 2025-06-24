from bs4 import BeautifulSoup
import dateparser 
from datetime import datetime
import os
import pandas as pd
import requests

YAHOO_URL = "https://finance.yahoo.com/topic/crypto/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
TIMEZONE = "America/Sao_Paulo"
CSV_NAME = "data.csv"

def load_news(CSV_NAME):
    archive = pd.read_csv(CSV_NAME)
    newsdict = archive.to_dict(orient="list")
    return newsdict

def fetch_html(URL):
    response = requests.get(URL, headers=HEADERS, timeout = 30)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch HTML content. Status code: {response.status_code}")
    return response.text

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_news(soup):
    '''
    Parses news titles, authors, and timestamps from the BeautifulSoup HTML.
    If a saved CSV exists, loads it and adds only new entries to avoid duplicates.
    Returns a dictionary containing the updated news data.
    '''
    h3_tags = soup.find_all('h3', class_='clamp yf-1jsv3x8')
    timestamp_tags = soup.find_all('div', class_="publishing yf-1weyqlp")
    
    newsdict = {
        "titles": [],
        "author": [],
        "timestamp": [],
        "fetch_timestamp": []
        }
    
    if os.path.exists(CSV_NAME):
        newsdict = load_news(CSV_NAME)
        existing_titles = set(newsdict["titles"])
    else: 
        existing_titles = set()

    if len(h3_tags) != len (timestamp_tags):
        raise Exception(f"Titles has {len(h3_tags)} entries but stamps has {len(timestamp_tags)}")
    
    
    for i in range(len(h3_tags)):
        title = h3_tags[i].get_text()
        stamp = timestamp_tags[i].get_text()
        stamp_parts = stamp.split("•")
        
        stamp_parts[0] = stamp_parts[0].strip()
        stamp_parts[1] = stamp_parts[1].strip()
        parsed_date = dateparser.parse(stamp_parts[1])

        
        if not parsed_date:
            raise ValueError(f"Failed to parse timestamp: '{stamp_parts[1]}'")

        
        if title not in existing_titles:
            newsdict["titles"].append(title)
            newsdict["author"].append(stamp_parts[0])
            newsdict["timestamp"].append(parsed_date)
            newsdict["fetch_timestamp"].append(datetime.now())
            #print(f"Appended | {title} | {parsed_date}")
        
    return newsdict
    
def create_df(newsdict):
    df = pd.DataFrame(newsdict)
    return df

#def change_timezone(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_localize(TIMEZONE)
    df["fetch_timestamp"] = pd.to_datetime(df["fetch_timestamp"]).dt.tz_localize(TIMEZONE)
    #return df
    
def generate_csv(df):
    df.to_csv(CSV_NAME, index = False)

def main():
    #1. Fetch html response
    fetched = fetch_html(YAHOO_URL)
   
    #2. Process the html 
    soup = parse_html(fetched)

    #3. Parse the news
    news_dict = get_news(soup)

    #4. Create DF
    df = create_df(news_dict)

    #5. Change timezone
    #df = change_timezone(df)

    #6. Print df
    #print(df)

    #7. Df to CSV
    generate_csv(df)

    return df

if __name__ == "__main__":
    main()