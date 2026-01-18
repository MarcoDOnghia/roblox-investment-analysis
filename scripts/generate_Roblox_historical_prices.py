import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# --- Configuration ---
# The directory where we will save our output files.
OUTPUT_DIR = "data"

# A dictionary to hold the simulation parameters for each item.
ITEMS = {
    "Dominus_Empyreus": {"initial_price": 1200000, "drift": 0.005, "volatility": 0.03},
    "Violet_Valkyrie": {"initial_price": 850000, "drift": 0.006, "volatility": 0.04},
    "Red_Valkyrie": {"initial_price": 700000, "drift": 0.004, "volatility": 0.035}
}

# The total number of weeks to simulate.
WEEKS_TO_SIMULATE = 159
# The start date for our simulated history.
# THIS IS THE CORRECTED LINE:
START_DATE_SIM = datetime.strptime("2023-01-01", "%Y-%m-%d")

def simulate_price_history(item_name, config):
    """
    Simulates a weekly price history for a single item using a geometric random walk.
    """
    prices = [config["initial_price"]]
    
    for _ in range(WEEKS_TO_SIMULATE - 1):
        weekly_return = config["drift"] + np.random.normal(0, config["volatility"])
        new_price = prices[-1] * (1 + weekly_return)
        prices.append(new_price)

    dates = [START_DATE_SIM + timedelta(weeks=i) for i in range(WEEKS_TO_SIMULATE)]

    df = pd.DataFrame({"Date": dates, "RAP": prices})
    df['RAP'] = df['RAP'].astype(int)
    df.set_index("Date", inplace=True)
    return df

def generate_all_simulations():
    """
    This is our main function. It runs the simulation for all configured items
    and saves the results to unique CSV files.
    """
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