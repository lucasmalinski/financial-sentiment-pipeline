# 📰 Crypto Sentiment Scanner — v1.1

A Python script that scrapes the latest cryptocurrency news headlines from Yahoo Finance, extracts timestamps, and matches them with the Bitcoin (BTC) price at the approximate moment of publication. Useful for tracking sentiment and price movement correlations over time.

---

## 🔧 Features

- ✅ Fetches live crypto news headlines from Yahoo Finance
- ✅ Parses timestamps like "27 minutes ago", "1 hour ago", and "yesterday"
- ✅ Retrieves historical BTC-USD prices via Yahoo Finance (`yfinance`)
- ✅ Outputs a structured CSV file with headlines, timestamps, and BTC price
- ✅ Single-file pipeline (`crypto_scan.py`)

---

## 📦 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
yfinance
beautifulsoup4
pandas
requests
```

---

## 🚀 How to Use

1. Run the script:

   ```bash
   python crypto_scan.py
   ```

2. The script will:

   - Fetch and save the latest HTML from Yahoo Finance
   - Parse headlines and timestamps
   - Convert relative timestamps into actual `datetime` values
   - Fetch the BTC price at those times
   - Save everything to a CSV: `financial_data_v1.1.csv`

3. Output example:

| headline                                        | timestamp           | btc\_price |
| ----------------------------------------------- | ------------------- | ---------- |
| "Is \$3,000 Within Reach for Ethereum in June?" | 2025-06-11 09:41:00 | 69,123.50  |

---

## 💂 Output

The resulting CSV file (`financial_data_v1.1.csv`) includes:

- `headline`: The news article title
- `timestamp`: Exact datetime parsed from relative expressions
- `btc_price`: Historical price of Bitcoin at that timestamp

---

## 🛠 Version History

- **v1.1**
  - Refactored: Merged HTML fetch and parse logic into one file
  - Replaced `pipeline.py` with unified `crypto_scan.py`
  - Cleaned up timestamp handling and BTC price lookup

---

## 🧠 Notes

- The BTC price lookup uses the closest minute interval available via Yahoo Finance.
- The script is meant for personal or research use. Frequent scraping may violate Yahoo's TOS.

---

## 📌 License

MIT License — use freely, but attribution is appreciated.

---

## 👤 Author

Lucas Malinski\
Built with ❤️ for crypto analysis and open-source learning.

