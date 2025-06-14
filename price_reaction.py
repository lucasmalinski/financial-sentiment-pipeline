import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from crypto_scan import get_btc_price_at  # your helper function

CSV_FILE = "financial_data_v1.0_debug.csv"
TICKER = "BTC-USD"
DATA_PERIOD = "2d"  # last 2 days should cover needed price intervals

# Define the columns to fill and their respective time offsets from parsed_timestamp
PRICE_COLUMNS = {
    'price_30m_after': timedelta(minutes=30),
    'price_1h_after': timedelta(hours=1),
    'price_6h_after': timedelta(hours=6)
}

import numpy as np

def main():
    df = pd.read_csv(CSV_FILE)
    df['parsed_timestamp'] = pd.to_datetime(df['parsed_timestamp'], errors='coerce')

    # Initialize price columns with NaN floats, NOT pd.NA
    for col in PRICE_COLUMNS.keys():
        if col not in df.columns:
            df[col] = np.nan

    df.sort_values('parsed_timestamp', ascending=False, inplace=True, ignore_index=True)

    btc_data = yf.download(TICKER, period=DATA_PERIOD, interval="30m")
    btc_data.index = btc_data.index.tz_localize(None)

    now = datetime.now()

    for idx, row in df.iterrows():
        base_time = row['parsed_timestamp']
        if pd.isna(base_time):
            continue

        for col_name, delta in PRICE_COLUMNS.items():
            if pd.isna(row[col_name]):
                target_time = base_time + delta
                if now >= target_time:
                    price = get_btc_price_at(target_time, btc_data)
                    if price is not None:
                        df.at[idx, col_name] = price

    # Force numeric dtypes for price columns before saving
    for col in PRICE_COLUMNS.keys():
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.to_csv(CSV_FILE, index=False, float_format='%.6f')
    print(f"✅ Prices updated and saved to {CSV_FILE}")


if __name__ == "__main__":
    main()
