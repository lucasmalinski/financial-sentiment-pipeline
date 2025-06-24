# Yahoo Finance Crypto News Scraper
### **This pipeline scrapes the latest crypto news from Yahoo Finance and saves it into a `data.csv` file.**

> This is a small project I built to get some hands-on practice with Python, web scraping, and getting started on some CI/CD. The main exercise was to reliably automate the entire process to fetch data every half hour 24/7.



---


One of the key learning goals here was to understand continuous integration workflows. That’s why you’ll see a `.github/workflows/` directory in the repo. It holds a scheduled GitHub Actions job to automate the script.

**Note on Timezones:** GitHub Actions runs in UTC. To ensure the `fetch_timestamp` matches your local time, you can set the `TZ` environment variable in the workflow. 
Example for São Paulo:
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Run scraper
        env:
          TZ: 'America/Sao_Paulo'
        run: python main.py
```

## What It Does

* **Scrapes Crypto News:** Collects article titles, authors, and publication times from the Yahoo Finance crypto page.
* **Deduplicates Entries:** Before saving, it checks `data.csv` and only appends new articles not already present.
* **Saves to CSV:** Organizes all the data in a clean `data.csv` file.
* **Runs Automatically:** A GitHub Actions workflow runs the scraper on a set schedule.

## Sample Output

Here’s what a few rows from `data.csv` look like:

```csv
titles,author,timestamp,fetch_timestamp
"Bitcoin jumps 5% amid Fed decision","CoinDesk","2025-06-23 17:10:00","2025-06-23 17:15:42"
"Ethereum upgrade sparks renewed interest","Yahoo Finance","2025-06-23 16:48:00","2025-06-23 17:15:42"
```

The `timestamp` reflects the publication time of the article, while `fetch_timestamp` logs when the data was collected.

## How It Works

The script is broken down into a few functions:

1. **Fetch:** Sends a request to the Yahoo URL, simulating a browser with a custom `User-Agent`.
2. **Parse:** Uses `BeautifulSoup4` to cleanly parse the HTML content.
3. **Extract & Clean:** Finds the `<h3>` and `<div>` tags holding article data. The site uses relative timestamps like "2 hours ago", so I use `dateparser` to convert them into proper `datetime` objects.
4. **Aggregate:** Loads previously saved articles (if any) from `data.csv` and skips any that are already stored.
5. **Save:** Uses `pandas` to convert everything to a DataFrame and save it back to `data.csv`.

## Running It Locally

**1. Install the dependencies:**

```bash
pip install pandas beautifulsoup4 requests dateparser
```

(Or use `pip install -r requirements.txt` if you're using the requirements file.)

## What's Next? (Roadmap)

Here are some future features I'd like to explore:

* **Price Integration:** Pull Bitcoin price at the time each article is published using yfinance.
* **Database Migration:** Switch from CSV to SQLite
* **Data Analysis:** As the dataset grows, it will serve me as a dataset for studying DS and ML.
