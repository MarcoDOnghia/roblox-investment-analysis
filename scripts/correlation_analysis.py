import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuration ---
OUTPUT_DIR = "data"
ROBLOX_ITEMS = ["Dominus_Empyreus", "Violet_Valkyrie", "Red_Valkyrie"]
STOCK_TICKERS = ["RBLX", "VWCE_DE"]

def analyze_correlations():
    """
    Computes correlation matrix between all assets.
    Creates heatmap visualization for portfolio diversification analysis.
    """
    print("=" * 70)
    print("🔗 CORRELATION ANALYZER - Portfolio Diversification Study")
    print("=" * 70)
    
    # Load returns data
    filepath = os.path.join(OUTPUT_DIR, "returns_calculated.csv")
    if not os.path.exists(filepath):
        print(f"❌ ERROR: {filepath} not found!")
        print("   Please run calculate_returns.py first.")
        return
    
    print(f"\n📥 Loading returns from {filepath}...")
    returns_df = pd.read_csv(filepath)
    
    # Build correlation matrix
    print("\n🧮 Computing Pearson correlation coefficients...")
    
    # Select only return columns
    return_cols = [col for col in returns_df.columns if col != 'Date']
    correlation_matrix = returns_df[return_cols].corr()
    
    # Clean up column names for display
    correlation_matrix.index = [col.replace('_Return', '') for col in correlation_matrix.index]
    correlation_matrix.columns = [col.replace('_Return', '') for col in correlation_matrix.columns]
    
    # Save correlation matrix
    output_path = os.path.join(OUTPUT_DIR, "correlation_matrix.csv")
    correlation_matrix.to_csv(output_path)
    
    print(f"\n✅ Correlation Matrix Computed:")
    print(correlation_matrix.round(3))
    print(f"\n   📄 Saved to: {output_path}")
    
    # Create heatmap visualization
    print("\n📊 Creating correlation heatmap...")
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt='.3f', cmap='coolwarm', 
                center=0, vmin=-1, vmax=1, square=True, cbar_kws={'label': 'Correlation'})
    plt.title('Asset Correlation Matrix\n(Negative = Diversification Benefit)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    heatmap_path = os.path.join(OUTPUT_DIR, "correlation_heatmap.png")
    plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
    print(f"   ✅ Heatmap saved to: {heatmap_path}")
    plt.close()
    
    # Analyze diversification potential
    print(f"\n{'=' * 70}")
    print("💡 DIVERSIFICATION ANALYSIS")
    print(f"{'=' * 70}\n")
    
    # Roblox vs Stocks correlation
    print("🎮 Roblox Items vs Stocks:")
    for item in ROBLOX_ITEMS:
        for ticker in STOCK_TICKERS:
            if item in correlation_matrix.index and ticker in correlation_matrix.columns:
                corr = correlation_matrix.loc[item, ticker]
                quality = "EXCELLENT ✨" if corr < 0.3 else "GOOD ✅" if corr < 0.5 else "MODERATE ⚠️" if corr < 0.7 else "POOR ❌"
                print(f"   {item} vs {ticker}: {corr:.3f} ({quality})")
    
    # Roblox vs Roblox correlation
    print("\n🎮 Roblox Items Correlation (within-asset risk):")
    for i, item1 in enumerate(ROBLOX_ITEMS):
        for item2 in ROBLOX_ITEMS[i+1:]:
            if item1 in correlation_matrix.index and item2 in correlation_matrix.columns:
                corr = correlation_matrix.loc[item1, item2]
                print(f"   {item1} vs {item2}: {corr:.3f}")
    
    # Stocks vs Stocks correlation
    print("\n📈 Stocks Correlation (market risk):")
    if len(STOCK_TICKERS) > 1:
        for i, ticker1 in enumerate(STOCK_TICKERS):
            for ticker2 in STOCK_TICKERS[i+1:]:
                if ticker1 in correlation_matrix.index and ticker2 in correlation_matrix.columns:
                    corr = correlation_matrix.loc[ticker1, ticker2]
                    print(f"   {ticker1} vs {ticker2}: {corr:.3f}")
    
    print(f"\n{'=' * 70}")
    print("📝 INTERPRETATION GUIDE:")
    print("   < 0.3  : EXCELLENT diversification (assets move independently)")
    print("   0.3-0.5: GOOD diversification (moderate benefit)")
    print("   0.5-0.7: MODERATE correlation (some co-movement)")
    print("   > 0.7  : POOR diversification (highly correlated)")
    print(f"{'=' * 70}\n")

if __name__ == "__main__":
    analyze_correlations()