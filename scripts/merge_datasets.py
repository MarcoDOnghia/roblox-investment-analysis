import pandas as pd
import os
from datetime import datetime

# --- Configuration ---
OUTPUT_DIR = "data"
ROBLOX_ITEMS = ["Dominus_Empyreus", "Violet_Valkyrie", "Red_Valkyrie"]
STOCK_TICKERS = {
    "rblx_prices": "RBLX",
    "vwce_de_prices": "VWCE_DE"
}

def merge_datasets():
    """
    Merges Roblox item prices (weekly) with stock prices (daily).
    Creates a master dataset with aligned dates and forward-filled Roblox data.
    """
    print("=" * 70)
    print("🔀 DATASET MERGER - Consolidating All Assets")
    print("=" * 70)
    
    # Load stock data (daily)
    print("\n📥 Loading stock data...")
    stock_data = {}
    for filename, ticker_name in STOCK_TICKERS.items():
        filepath = os.path.join(OUTPUT_DIR, f"{filename}.csv")
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df['Date'] = pd.to_datetime(df['Date'])
            stock_data[ticker_name] = df.set_index('Date')[['Close']]
            print(f"   ✅ {ticker_name}: {len(df)} records")
        else:
            print(f"   ⚠️  {ticker_name}: File not found at {filepath}")
    
    # Load Roblox item data (weekly)
    print("\n📥 Loading Roblox item data...")
    roblox_data = {}
    for item in ROBLOX_ITEMS:
        filepath = os.path.join(OUTPUT_DIR, f"{item.lower()}_prices.csv")
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            df['Date'] = pd.to_datetime(df['Date'])
            roblox_data[item] = df.set_index('Date')[['RAP']]
            print(f"   ✅ {item}: {len(df)} records")
        else:
            print(f"   ⚠️  {item}: File not found at {filepath}")
    
    if not stock_data or not roblox_data:
        print("\n❌ ERROR: Missing required data files!")
        return
    
    # Combine all data
    print("\n🔗 Merging all datasets...")
    all_data = {}
    
    # Add stocks
    for ticker_name, data_df in stock_data.items():
        all_data[ticker_name] = data_df
    
    # Add Roblox items
    for item_name, data_df in roblox_data.items():
        all_data[item_name] = data_df
    
    # Create master dataframe (outer join on dates)
    master_df = pd.DataFrame()
    for asset_name, data_df in all_data.items():
        if master_df.empty:
            master_df = data_df.copy()
            master_df.columns = [asset_name]
        else:
            master_df = master_df.join(data_df, how='outer')
            master_df = master_df.rename(columns={list(data_df.columns)[0]: asset_name})
    
    # Sort by date
    master_df = master_df.sort_index()
    
    # Forward-fill Roblox data (weekly to daily alignment)
    for item in ROBLOX_ITEMS:
        if item in master_df.columns:
            master_df[item] = master_df[item].fillna(method='ffill')
    
    # Drop rows where ANY stock data is missing (stocks are our anchor)
    master_df = master_df.dropna(subset=list(STOCK_TICKERS.values()))
    
    # Reset index to make Date a column
    master_df = master_df.reset_index()
    
    # Save to CSV
    output_path = os.path.join(OUTPUT_DIR, "merged_master.csv")
    master_df.to_csv(output_path, index=False)
    
    print(f"\n✅ SUCCESS: Master dataset created")
    print(f"   📄 File: {output_path}")
    print(f"   📊 Total rows: {len(master_df)}")
    print(f"   📅 Date range: {master_df['Date'].iloc[0]} to {master_df['Date'].iloc[-1]}")
    print(f"   🎯 Assets included: {', '.join(master_df.columns[1:])}")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    merge_datasets()