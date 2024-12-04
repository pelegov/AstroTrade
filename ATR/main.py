from datetime import datetime, timedelta
from atr import process_tickers
import pandas as pd
import os

if __name__ == "__main__":
    # Define dates
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

    # Path to the ticker file
    file_path = "./tickerlist.txt"

    # Process tickers and calculate ATR
    results = process_tickers(file_path, start_date, end_date, window=14)

    if results:
        # Extract the last row (latest ATR) for each ticker
        simplified_data = []
        for ticker, data in results.items():
            if not data.empty:
                last_row = data.iloc[-1]  # Get the last row
                simplified_data.append({
                    "Ticker": ticker,
                    "Date": last_row.name.strftime('%Y-%m-%d'),
                    "Close": float(last_row["Close"]),
                    "ATR": float(last_row["ATR"]), 
                })


        # Convert to DataFrame
        final_data = pd.DataFrame(simplified_data)

        # Set output directory
        output_dir = os.getenv("OUTPUT_DIR", "./output")  # Default to "./output" if OUTPUT_DIR is not set
        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
        
        # Set output file path
        output_file = os.path.join(output_dir, "tickers_atr.csv")

        # Save the simplified data to a CSV file
        final_data.to_csv(output_file, index=False)  # Save without index column
        print(f"Saved simplified data to {output_file}")
    else:
        print("No data to process.")
