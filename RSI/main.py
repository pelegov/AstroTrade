from datetime import datetime, timedelta
from rsi import process_tickers

if __name__ == "__main__":
    # Define dates
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365 * 2)).strftime('%Y-%m-%d')

    # Path to the ticker file
    file_path = "./tickerlist.txt"

    # Process tickers
    results = process_tickers(file_path, start_date, end_date)

    if not results.empty:
        print("Results successfully processed and saved.")
    else:
        print("No data to process.")