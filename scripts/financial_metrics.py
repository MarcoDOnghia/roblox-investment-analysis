import pandas as pd
import numpy as np
import os

# --- Configuration ---
OUTPUT_DIR = "data"
RISK_FREE_RATE = 0.04  # 4% annual risk-free rate (2026 US Treasury)
TRADING_DAYS_YEAR = 252
WEEKS_YEAR = 52

ROBLOX_ITEMS = ["Dominus_Empyreus", "Violet_Valkyrie", "Red_Valkyrie"]
STOCK_TICKERS = ["RBLX", "VWCE_DE"]

def calculate_financial_metrics():
    """
    Calculates:
    - Annual Returns
    - Annualized Volatility
    - Sharpe Ratios
    - Risk-adjusted performance comparison
    """
    print("=" * 70)
    print("💰 FINANCIAL METRICS CALCULATOR")
    print("=" * 70)
    
    # Load returns data
    filepath = os.path.join(OUTPUT_DIR, "returns_calculated.csv")
    if not os.path.exists(filepath):
        print(f"❌ ERROR: {filepath} not found!")
        print("   Please run calculate_returns.py first.")
        return
    
    print(f"\n📥 Loading returns from {filepath}...")
    returns_df = pd.read_csv(filepath)
    
    # Initialize results dataframe
    metrics = []
    
    # Process Roblox items (weekly data -> annualize by √52)
    print("\n🎮 Processing Roblox Items (weekly data)...")
    for item in ROBLOX_ITEMS:
        col = f'{item}_Return'
        if col in returns_df.columns:
            returns = returns_df[col].dropna()
            
            # Annual return: (1 + mean_weekly_return)^52 - 1
            mean_weekly_return = returns.mean()
            annual_return = (1 + mean_weekly_return) ** WEEKS_YEAR - 1
            
            # Annualized volatility: std_dev_weekly * √52
            weekly_volatility = returns.std()
            annual_volatility = weekly_volatility * np.sqrt(WEEKS_YEAR)
            
            # Sharpe ratio: (Annual Return - Risk Free Rate) / Annual Volatility
            sharpe_ratio = (annual_return - RISK_FREE_RATE) / annual_volatility if annual_volatility > 0 else 0
            
            metrics.append({
                'Asset': item,
                'Type': 'Roblox Item',
                'Annual_Return_%': round(annual_return * 100, 2),
                'Annual_Volatility_%': round(annual_volatility * 100, 2),
                'Sharpe_Ratio': round(sharpe_ratio, 3),
                'Data_Points': len(returns),
                'Mean_Weekly_Return_%': round(mean_weekly_return * 100, 3)
            })
            
            print(f"   ✅ {item}")
            print(f"      Return: {annual_return*100:.2f}% | Volatility: {annual_volatility*100:.2f}% | Sharpe: {sharpe_ratio:.3f}")
    
    # Process stocks (daily data -> annualize by √252)
    print("\n📈 Processing Stocks (daily data)...")
    for ticker in STOCK_TICKERS:
        col = f'{ticker}_Return'
        if col in returns_df.columns:
            returns = returns_df[col].dropna()
            
            # Annual return: (1 + mean_daily_return)^252 - 1
            mean_daily_return = returns.mean()
            annual_return = (1 + mean_daily_return) ** TRADING_DAYS_YEAR - 1
            
            # Annualized volatility: std_dev_daily * √252
            daily_volatility = returns.std()
            annual_volatility = daily_volatility * np.sqrt(TRADING_DAYS_YEAR)
            
            # Sharpe ratio
            sharpe_ratio = (annual_return - RISK_FREE_RATE) / annual_volatility if annual_volatility > 0 else 0
            
            metrics.append({
                'Asset': ticker,
                'Type': 'Stock',
                'Annual_Return_%': round(annual_return * 100, 2),
                'Annual_Volatility_%': round(annual_volatility * 100, 2),
                'Sharpe_Ratio': round(sharpe_ratio, 3),
                'Data_Points': len(returns),
                'Mean_Daily_Return_%': round(mean_daily_return * 100, 3)
            })
            
            print(f"   ✅ {ticker}")
            print(f"      Return: {annual_return*100:.2f}% | Volatility: {annual_volatility*100:.2f}% | Sharpe: {sharpe_ratio:.3f}")
    
    # Create metrics dataframe
    metrics_df = pd.DataFrame(metrics)
    
    # Save to CSV
    output_path = os.path.join(OUTPUT_DIR, "financial_metrics.csv")
    metrics_df.to_csv(output_path, index=False)
    
    # Display results
    print(f"\n{'=' * 70}")
    print("📊 FINANCIAL METRICS SUMMARY")
    print(f"{'=' * 70}")
    print(f"\nRisk-Free Rate Used: {RISK_FREE_RATE*100}%\n")
    print(metrics_df.to_string(index=False))
    
    # Key insights
    print(f"\n{'=' * 70}")
    print("💡 KEY INSIGHTS")
    print(f"{'=' * 70}")
    
    best_sharpe = metrics_df.loc[metrics_df['Sharpe_Ratio'].idxmax()]
    worst_volatility = metrics_df.loc[metrics_df['Annual_Volatility_%'].idxmax()]
    
    print(f"\n✨ Best Risk-Adjusted Return (Sharpe):")
    print(f"   {best_sharpe['Asset']}: {best_sharpe['Sharpe_Ratio']}")
    print(f"\n⚠️  Highest Volatility (Risk):")
    print(f"   {worst_volatility['Asset']}: {worst_volatility['Annual_Volatility_%']}%")
    
    print(f"\n{'=' * 70}\n")

if __name__ == "__main__":
    calculate_financial_metrics()