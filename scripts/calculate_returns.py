import pandas as pd
import numpy as np
import os

# --- Configuration ---
OUTPUT_DIR = "data"
ROBLOX_ITEMS = ["Dominus_Empyreus", "Violet_Valkyrie", "Red_Valkyrie"]
STOCK_TICKERS = ["RBLX", "VWCE_DE"]

def calculate_returns():
    """
    Calculates percentage returns for all assets from merged dataset.
    Returns = (Price_t - Price_t-1) / Price_t-1
    """
    print("=" * 70)
    print("📈 RETURNS CALCULATOR - Computing Asset Returns")
    print("=" * 70)
    
    # Load merged master dataset
    filepath = os.path.join(OUTPUT_DIR, "merged_master.csv")
    if not os.path.exists(filepath):
        print(f"❌ ERROR: {filepath} not found!")
        print("   Please run merge_datasets.py first.")
        return
    
    print(f"\n📥 Loading merged dataset from {filepath}...")
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    
    print(f"   ✅ Loaded {len(df)} records, {len(df.columns)-1} assets")
    
    # Calculate returns for each asset
    print("\n🧮 Calculating returns...")
    returns_df = df[['Date']].copy()
    
    # Roblox items (weekly data)
    for item in ROBLOX_ITEMS:
        if item in df.columns:
            returns_df[f'{item}_Return'] = df[item].pct_change()
            print(f"   ✅ {item}: Return column created")
    
    # Stock tickers (daily data)
    for ticker in STOCK_TICKERS:
        if ticker in df.columns:
            returns_df[f'{ticker}_Return'] = df[ticker].pct_change()
            print(f"   ✅ {ticker}: Return column created")
    
    # Remove first row (NaN returns)
    returns_df = returns_df.dropna(subset=[col for col in returns_df.columns if col != 'Date'])
    
    # Save to CSV
    output_path = os.path.join(OUTPUT_DIR, "returns_calculated.csv")
    returns_df.to_csv(output_path, index=False)
    
    print(f"\n✅ SUCCESS: Returns calculated")
    print(f"   📄 File: {output_path}")
    print(f"   📊 Total rows: {len(returns_df)}")
    print(f"   📊 Sample returns (first 5 rows):")
    print(returns_df.head())
    print("\n" + "=" * 70)

if __name__ == "__main__":
    calculate_returns()