import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# --- Configuration ---
OUTPUT_DIR = "data"

# A dictionary to hold the simulation parameters for each item.
ITEMS = {
    "Dominus_Empyreus": {"initial_price": 1200000, "drift": 0.005, "volatility": 0.03},
    "Violet_Valkyrie": {"initial_price": 850000, "drift": 0.006, "volatility": 0.04},
    "Red_Valkyrie": {"initial_price": 700000, "drift": 0.004, "volatility": 0.035}
}

WEEKS_TO_SIMULATE = 159
TART_DATE_SIM = datetime.strptime("2023-01-01", "%Y-%m-%d")

def simulate_price_history(item_name, config):
   prices = [config["initial_price"]]
    
for _ in range(WEEKS_TO_SIMULATE - 1):
        weekly_return = config["drift"] + np.random.normal(0, config["volatility"])
        new_price = prices[-1] * (1 + weekly_return)
        prices.append(new_price)
        
        dates = [TART_DATE_SIM + timedelta(weeks=i) for i in range(WEEKS_TO_SIMULATE)]
      
        df = pd.DataFrame({"Date": dates, "RAP": prices})
        df['RAP'] = df['RAP'].astype(int)
        df.set_index("Date", inplace=True)
return df

def generate_all_simulations():
    print("\n--- Starting Task 1.4: Simulate Roblox Historical Prices ---")
    
    for item, params in ITEMS.items():
        print(f"Simulating price history for {item}...")
        try:
            price_df = simulate_price_history(item, params)
            output_path = os.path.join(OUTPUT_DIR, f"{item.lower()}_prices.csv")
            price_df.to_csv(output_path)
            print(f"✅ Successfully saved simulated data for {item} to {output_path}")
        except Exception as e:
            print(f"❌ An error occurred during simulation for {item}: {e}")

    print("\n--- Roblox item price simulation complete. ---")

if __name__ == "__main__":
    generate_all_simulations()