import yfinance as yf
import pandas as pd
import os

def process_tickers(file_path, start_date, end_date):
    """
    Process tickers to identify Golden and Death Cross events.

    Parameters:
        file_path (str): Path to the ticker list file.
        start_date (str): Start date for fetching data.
        end_date (str): End date for fetching data.

    Returns:
        pd.DataFrame: DataFrame with Golden and Death Cross events.
    """
    # Read tickers from file
    with open(file_path, "r") as file:
        tickers = file.read().splitlines()

    result = []

    for ticker in tickers:
        print(f"{ticker} in process")

        # Download Data for ticker
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            print(f"No data found for {ticker}. Skipping.")
            continue

        # Calculate moving averages
        data['SMA50'] = data['Close'].rolling(window=50).mean()
        data['SMA200'] = data['Close'].rolling(window=200).mean()

        # Identify Golden and Death Cross
        data['Golden_Cross'] = (data['SMA50'] > data['SMA200']) & (data['SMA50'].shift(1) <= data['SMA200'].shift(1))
        data['Death_Cross'] = (data['SMA50'] < data['SMA200']) & (data['SMA50'].shift(1) >= data['SMA200'].shift(1))

        # Save results
        golden_cross_dates = data[data['Golden_Cross']].index
        death_cross_dates = data[data['Death_Cross']].index

        for date in golden_cross_dates:
            result.append({"Ticker": ticker, "Date": date.strftime('%Y-%m-%d'), "Type": "Golden Cross"})
        for date in death_cross_dates:
            result.append({"Ticker": ticker, "Date": date.strftime('%Y-%m-%d'), "Type": "Death Cross"})

    # Convert results to DataFrame
    results_df = pd.DataFrame(result)

    # Save results to CSV
    output_dir = os.getenv("OUTPUT_DIR", "./output")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "cross_events.csv")
    results_df.to_csv(output_file, index=False)
    print(f"File saved to: {output_file}")

    return results_df
