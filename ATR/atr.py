from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import os

def calculate_atr(data, window=14):
    """Function to calculate ATR (Average True Range) for a given DataFrame."""
    data['tr1'] = data['High'] - data['Low']
    data['tr2'] = abs(data['High'] - data['Close'].shift(1))
    data['tr3'] = abs(data['Low'] - data['Close'].shift(1))
    data['TR'] = data[['tr1', 'tr2', 'tr3']].max(axis=1)
    data['ATR'] = data['TR'].rolling(window=window).mean()
    data.drop(['tr1', 'tr2', 'tr3'], axis=1, inplace=True)
    return data

def process_tickers(file_path, start_date, end_date, window=14):
    """Processes multiple tickers from a file and calculates ATR for each."""
    with open(file_path, "r") as file:
        tickers = file.read().splitlines()

    all_data = {}  # Dictionary to store data for each ticker

    for index, ticker in enumerate(tickers):
        print(f"{ticker} in process")
        
        # Download data for the ticker
        data = yf.download(ticker, start=start_date, end=end_date)

        if data.empty:
            print(f"No data found for {ticker}. Skipping.")
            continue

        # Calculate ATR
        try:
            data = calculate_atr(data, window)
            all_data[ticker] = data  # Store the processed data
            print(data[['High', 'Low', 'Close', 'ATR']].tail())  # Display last few rows
        except Exception as e:
            print(f"Error processing ATR for {ticker}: {e}")
            continue

    return all_data
