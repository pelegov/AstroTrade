import yfinance as yf
import pandas as pd
import os
from ta.momentum import RSIIndicator


def process_tickers(file_path, start_date, end_date, window=14):
    """Processes multiple tickers from a file and saves only the last day's RSI data."""
    # Read tickers from file
    with open(file_path, "r") as file:
        tickers = file.read().splitlines()

    results = []

    for ticker in tickers:
        print(f"{ticker} in process")
        
        # Download data
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            print(f"No data found for {ticker}. Skipping.")
            continue

        # Ensure 'Close' is a Series
        close_prices = data['Close'].squeeze()  # Converts to 1D if needed

        # Calculate RSI
        rsi = RSIIndicator(close=close_prices, window=window)
        data['RSI'] = rsi.rsi()

        # Save only the last row
        last_row = data.iloc[-1]
        results.append({
            "Ticker": ticker,
            "Date": last_row.name.strftime('%Y-%m-%d'),
            "Close": float(last_row['Close'].iloc[0] if isinstance(last_row['Close'], pd.Series) else last_row['Close']),
            "RSI": float(last_row['RSI'].iloc[0] if isinstance(last_row['RSI'], pd.Series) else last_row['RSI'])
        })

    # Convert results to DataFrame
    results_rsi = pd.DataFrame(results)

    # Save results to CSV
    output_dir = os.getenv("OUTPUT_DIR", "./output")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "RSI.csv")
    results_rsi.to_csv(output_file, index=False)
    print(f"File saved to: {output_file}")

    return results_rsi
