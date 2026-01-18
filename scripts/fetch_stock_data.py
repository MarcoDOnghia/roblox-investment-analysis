import yfinance as yf
import pandas as pd
import os

# --- Configuration ---
# A list of the stock tickers you want to download.
TICKERS = ["RBLX", "VWCE.DE"]
# The start and end dates for the historical data.
START_DATE = "2023-01-01"
END_DATE = "2026-01-18"
# The name of the folder where the output files will be saved.
OUTPUT_DIR = "data"

def fetch_stock_data():
    """
    This is our main function. It creates the output directory if needed,
    then loops through the TICKERS list and downloads the data for each one.
    """
    # First, check if the output directory exists.
    if not os.path.exists(OUTPUT_DIR):
        # If it doesn't exist, create it.
        print(f"Directory '{OUTPUT_DIR}' not found. Creating it now...")
        os.makedirs(OUTPUT_DIR)

    print("--- Starting Data Fetching Process ---")
    
    # This loop will run once for "RBLX" and once for "VWCE.DE".
    for ticker in TICKERS:
        # A try/except block is used to prevent the script from crashing
        # if there's a network error or a problem with one specific ticker.
        try:
            # --- All actions that might fail go inside the 'try' block. ---
            
            print(f"Fetching data for ticker: {ticker}...")
            
            # 1. Download the data from Yahoo Finance.
            data = yf.download(ticker, start=START_DATE, end=END_DATE)

            # 2. Check if the download was successful. Sometimes yfinance
            # returns an empty table (DataFrame) if the ticker is wrong
            # or there's no data for the requested dates.
            if data.empty:
                print(f"⚠️  Warning: No data was returned for {ticker}. Skipping file save.")
                # 'continue' immediately stops this iteration of the loop
                # and jumps to the next ticker.
                continue

            # 3. Create a clean filename (e.g., "rblx_prices.csv").
            filename = f"{ticker.lower()}_prices.csv"
            # 4. Safely join the directory and filename to create the full path.
            output_path = os.path.join(OUTPUT_DIR, filename)

            # 5. Save the downloaded data table to the CSV file.
            data.to_csv(output_path)
            
            print(f"✅  Success! Data for {ticker} saved to {output_path}")

        # If any line inside the 'try' block causes an error,
        # the program will immediately jump here.
        except Exception as e:
            # This will print a helpful error message without crashing the script.
            print(f"❌ ERROR: An error occurred for ticker {ticker}. Reason: {e}")

# This special block ensures the script runs our main function
# when you execute the file directly from the terminal.
if __name__ == "__main__":
    fetch_stock_data()