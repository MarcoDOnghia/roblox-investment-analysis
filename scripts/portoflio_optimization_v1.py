import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt

# --- Configuration ---
OUTPUT_DIR = "data"
RISK_FREE_RATE = 0.04  # 4% annual risk-free rate (2026 US Treasury)
NUMBER_OF_PORTFOLIOS = 10000
np.random.seed(42)  # For reproducibility

ASSETS = ["Dominus_Empyreus", "Violet_Valkyrie", "Red_Valkyrie", "RBLX", "VWCE_DE"]
ROBLOX_ITEMS = ["Dominus_Empyreus", "Violet_Valkyrie", "Red_Valkyrie"]
STOCKS = ["RBLX", "VWCE_DE"]

def load_financial_data():

    print("Loading financial data...")
    metrics_path = os.path.join(OUTPUT_DIR, "financial_metrics.csv")
    correlation_path = os.path.join(OUTPUT_DIR, "correlation_matrix.csv")

    if not os.path.exists(metrics_path) or not os.path.exists(correlation_path):

        print("ERROR: Required financial data files not found!")
        print("Please run financial_metrics.py and correlation_analysis.py first")
        return None,None,None
    
    metrics_df = pd.read_csv(metrics_path)
    metrics_dict = {}
    for _, row in metrics_df.iterrows():
        assets = row['Asset']
        metrics_dict[assets] = {
            'return':row['Annual_Return_%'] / 100,
            'volatility':row['Annual_Volatility_%'] / 100
        }
    
    corr_matrix = pd.read_csv(correlation_path, index_col=0)
    return metrics_dict, corr_matrix

def build_covariance_matrix(metrics_dict,corr_matrix):

    # Formula: Covariance(i,j) = Correlation(i,j) × Volatility(i) × Volatility(j)

    print("\n" + "="*80)
    print ("Building covariance matrix...")
    print("="*80)

    volatilities = np.array([metrics_dict[assets]['volatility'] for assets in ASSETS])

    print ("\n Volatilities in order of assets:")
    for assets, vol in zip(ASSETS, volatilities):
        print (f" {assets}: {vol*100:.2f}%")

    corr_values =corr_matrix.values

    cov_matrix = corr_values * np.outer(volatilities,volatilities)

    print (f"\n Covariance matrix (5x5):")
    cov_df = pd.DataFrame(cov_matrix, index=ASSETS, columns=ASSETS)
    print(cov_df.round(6))

    return cov_matrix

def calculate_portfolio_metrics (weights, metrics_dict, cov_matrix):
    # weights = array of allocation percentages
    # metrics_dict = dictionary with asset returns and volatilities
    # cov_matrix = the covariance matrix built earlier

    weights = np.array(weights)
    
    # Calculate portfolio expected return = sum of (weight × return) for each asset
    portfolio_return = np.sum(weights* np.array([metrics_dict[asset]['return'] for asset in ASSETS]))

    # Formula: volatility = sqrt(weights^T × covariance_matrix × weights)                        
    portfolio_volatility = np.sqrt (np.dot(weights, np.dot (cov_matrix, weights)))

    #Calculate Sharpe ratio = (portfolio return - risk free rate) / portfolio volatility

    if portfolio_volatility > 0:
        sharpe_ratio = (portfolio_return - RISK_FREE_RATE) / portfolio_volatility

    else:
        sharpe_ratio = 0
    
    return portfolio_return, portfolio_volatility, sharpe_ratio

def generate_random_portfolios (metrics_dict, cov_matrix):

    print("\n" + "="*80)
    print ("Generating random portfolios...")
    print("="*80)

    results = np.zeros((3, NUMBER_OF_PORTFOLIOS))

    weights_record =[]

    for i in range(NUMBER_OF_PORTFOLIOS):

        random_weights = np.random.random(len(ASSETS))

        normalized_weights = random_weights / np.sum(random_weights)

        weights_record.append(normalized_weights)   

        p_return, p_volatility, p_sharpe = calculate_portfolio_metrics(normalized_weights, metrics_dict, cov_matrix)

        results[0,i] = p_return
        results[1,i] = p_volatility
        results[2,i] = p_sharpe
        
        if (i + 1) % 1000 == 0:
            print(f" Generated {i + 1:,} portfolios...")

    weights_array = np.array(weights_record)
    
    return results, weights_array

def find_optimal_portfolios(metrics_dict, cov_matrix):
    print("\n" + "="*80)
    print("Finding optimal portfolios...")
    print("="*80)
    
    results, weights_array = generate_random_portfolios(metrics_dict, cov_matrix)
    
    # Find index of portfolio with minimum volatility
    min_vol_idx = np.argmin(results[1])
    
    # Find index of portfolio with maximum Sharpe ratio
    max_sharpe_idx = np.argmax(results[2])
    
    # Extract metrics for Minimum Variance portfolio
    min_vol_return = results[0, min_vol_idx]
    min_vol_volatility = results[1, min_vol_idx]
    min_vol_sharpe = results[2, min_vol_idx]
    min_vol_weights = weights_array[min_vol_idx]
    
    # Extract metrics for Maximum Sharpe Ratio portfolio
    max_sharpe_return = results[0, max_sharpe_idx]
    max_sharpe_volatility = results[1, max_sharpe_idx]
    max_sharpe_sharpe = results[2, max_sharpe_idx]
    max_sharpe_weights = weights_array[max_sharpe_idx]
    
    return {
        'min_vol': {
            'return': min_vol_return,
            'volatility': min_vol_volatility,
            'sharpe_ratio': min_vol_sharpe,
            'weights': min_vol_weights
        },
        'max_sharpe': {
            'return': max_sharpe_return,
            'volatility': max_sharpe_volatility,
            'sharpe_ratio': max_sharpe_sharpe,
            'weights': max_sharpe_weights
        }
    }, results, weights_array

def format_weights(weights):

    return {asset: weight for asset, weight in zip(ASSETS, weights)}
        
    
def calculate_portfolio_metrics(weights, metrics_dict, cov_matrix):

        weights = np.array(weights)

        # Formula: Portfolio Return = Sum of (weight × individual return) for each asset

        portfolio_return = np.sum (weights*np.array([metrics_dict[asset]['return'] for asset in ASSETS]))

        # Formula: Portfolio Volatility = sqrt(w^T × Cov × w)

        portfolio_volatility = np.sqrt (np.dot(weights, np.dot(cov_matrix, weights)))


        if portfolio_volatility > 0:

            # Formula: Sharpe Ratio = (Portfolio Return - Risk Free Rate) / Portfolio Volatility
            sharpe_ratio = (portfolio_return - RISK_FREE_RATE) / portfolio_volatility
        else:
            sharpe_ratio = 0
        
        return portfolio_return, portfolio_volatility, sharpe_ratio 

def plot_efficient_frontier(all_results, optimal_portfolios):
    
    returns = all_results[0] * 100      # Convert to percentage
    volatilities = all_results[1] * 100  # Convert to percentage
    sharpe_ratios = all_results[2]
    
    plt.figure(figsize=(14, 8))
    
    scatter = plt.scatter(
        volatilities,           # X-axis: Risk
        returns,               # Y-axis: Return
        c=sharpe_ratios,       # Color by Sharpe ratio
        cmap='viridis',        # Color scheme (purple to yellow)
        alpha=0.5,             # Transparency
        s=10,                  # Point size
        edgecolors='none'
    )
    
    # Add colorbar to show Sharpe ratio scale
    cbar = plt.colorbar(scatter, label='Sharpe Ratio')
    
    min_vol = optimal_portfolios['min_vol']
    max_sharpe = optimal_portfolios['max_sharpe']
    
    # Plot Minimum Variance Portfolio (Red dot)
    plt.scatter(
        min_vol['volatility'] * 100,  # X: volatility
        min_vol['return'] * 100,       # Y: return
        marker='o',
        color='red',
        s=300,                         # Larger size
        edgecolors='darkred',
        linewidths=2,
        label=f"Min Variance\n(Return: {min_vol['return']*100:.2f}%, Risk: {min_vol['volatility']*100:.2f}%)",
        zorder=5
    )
    
    # Plot Maximum Sharpe Ratio Portfolio (Green dot)
    plt.scatter(
        max_sharpe['volatility'] * 100,  # X: volatility
        max_sharpe['return'] * 100,      # Y: return
        marker='*',
        color='lime',
        s=1000,                          # Even larger
        edgecolors='darkgreen',
        linewidths=2,
        label=f"Max Sharpe\n(Return: {max_sharpe['return']*100:.2f}%, Risk: {max_sharpe['volatility']*100:.2f}%)",
        zorder=5
    )
    
    plt.xlabel('Annual Volatility (Risk) %', fontsize=12, fontweight='bold')
    plt.ylabel('Expected Annual Return %', fontsize=12, fontweight='bold')
    plt.title('Efficient Frontier: Portfolio Optimization Analysis\n(10,000 Random Portfolios)', 
              fontsize=14, fontweight='bold')
    
    plt.legend(loc='upper left', fontsize=11, framealpha=0.95)
    
    plt.grid(True, alpha=0.3, linestyle='--')
    
    output_path = os.path.join(OUTPUT_DIR, "efficient_frontier_plot.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Efficient frontier plot saved to: {output_path}")
    
    # Show the plot
    plt.show()

def main():

    print("="*80)
    print("PORTFOLIO OPTIMIZATION - EFFICIENT FRONTIER & OPTIMAL ALLOCATIONS")
    print("="*80)

    metrics_dict, corr_matrix = load_financial_data()

    if metrics_dict is None or corr_matrix is None:
        return print("Failed to load financial data. Exiting.")
    
    print("Financial data loaded successfully.")

    cov_matrix = build_covariance_matrix(metrics_dict, corr_matrix)
    optimal_portfolios, all_results, all_weights = find_optimal_portfolios(metrics_dict, cov_matrix)

    min_vol = optimal_portfolios['min_vol']
    max_sharpe = optimal_portfolios['max_sharpe']   

    print("\n" + "="*80)
    print("Optimal Portfolios Found:")
    print("="*80)

    print("\n Minimum Variance Portfolio:")
    print("-"*80)
    min_vol_weights_dict = format_weights(min_vol['weights'])

    print(f"  Expected Annual Return: {min_vol['return']*100:.2f}%")
    print(f"  Annualized Volatility: {min_vol['volatility']*100:.2f}%")
    print(f"  Sharpe Ratio: {min_vol['sharpe_ratio']:.4f}")
    print(f"\n Asset Allocation:")

    for asset, weight in min_vol_weights_dict.items():
        allocation_pct = weight * 100

        if allocation_pct > 0.01:
            bar = '█' * int(allocation_pct // 2)
            print(f"   {asset:25s}: {allocation_pct:6.2f}% | {bar}")

    print("\n Maximum Sharpe Ratio Portfolio:")
    print("-"*80)
    max_sharpe_weights_dict = format_weights(max_sharpe['weights'])

    print(f"  Expected Annual Return: {max_sharpe['return']*100:.2f}%")
    print(f"  Annualized Volatility: {max_sharpe['volatility']*100:.2f}%")
    print(f"  Sharpe Ratio: {max_sharpe['sharpe_ratio']:.4f}")
    print(f"\n Asset Allocation:")

    for asset, weight in max_sharpe_weights_dict.items():
        allocation_pct = weight * 100

        if allocation_pct > 0.01:
            bar = '█' * int(allocation_pct // 2)
            print(f"   {asset:25s}: {allocation_pct:6.2f}% | {bar}")

    plot_efficient_frontier(all_results, optimal_portfolios)
    
    print("\n" + "="*80)
    print("ROBLOX ITEMS vs TRADITIONAL STOCKS")
    print("="*80)
    
    roblox_weight_min = sum([min_vol_weights_dict[item] for item in ROBLOX_ITEMS if item in min_vol_weights_dict]) * 100
    stocks_weight_min = sum([min_vol_weights_dict[ticker] for ticker in STOCKS if ticker in min_vol_weights_dict]) * 100
    
    roblox_weight_max = sum([max_sharpe_weights_dict[item] for item in ROBLOX_ITEMS if item in max_sharpe_weights_dict]) * 100
    stocks_weight_max = sum([max_sharpe_weights_dict[ticker] for ticker in STOCKS if ticker in max_sharpe_weights_dict]) * 100
    
    print(f"\nMinimum Variance Portfolio:")
    print(f"  Roblox Items:      {roblox_weight_min:6.2f}%")
    print(f"  Traditional Stocks: {stocks_weight_min:6.2f}%")
    
    print(f"\nMaximum Sharpe Portfolio:")
    print(f"  Roblox Items:      {roblox_weight_max:6.2f}%")
    print(f"  Traditional Stocks: {stocks_weight_max:6.2f}%")
    
    print("\n" + "="*80)
    print("💾SAVING RESULTS TO CSV")
    print("="*80)
    
    optimal_summary = pd.DataFrame([
        {
            'Portfolio_Type': 'Minimum Variance',
            'Expected_Return_%': min_vol['return'] * 100,
            'Volatility_%': min_vol['volatility'] * 100,
            'Sharpe_Ratio': min_vol['sharpe_ratio'],
            'Dominus_Empyreus_%': min_vol_weights_dict.get('Dominus_Empyreus', 0) * 100,
            'Violet_Valkyrie_%': min_vol_weights_dict.get('Violet_Valkyrie', 0) * 100,
            'Red_Valkyrie_%': min_vol_weights_dict.get('Red_Valkyrie', 0) * 100,
            'RBLX_%': min_vol_weights_dict.get('RBLX', 0) * 100,
            'VWCE_DE_%': min_vol_weights_dict.get('VWCE_DE', 0) * 100,
            'Roblox_Total_%': roblox_weight_min,
            'Stocks_Total_%': stocks_weight_min
        },
        {
            'Portfolio_Type': 'Maximum Sharpe',
            'Expected_Return_%': max_sharpe['return'] * 100,
            'Volatility_%': max_sharpe['volatility'] * 100,
            'Sharpe_Ratio': max_sharpe['sharpe_ratio'],
            'Dominus_Empyreus_%': max_sharpe_weights_dict.get('Dominus_Empyreus', 0) * 100,
            'Violet_Valkyrie_%': max_sharpe_weights_dict.get('Violet_Valkyrie', 0) * 100,
            'Red_Valkyrie_%': max_sharpe_weights_dict.get('Red_Valkyrie', 0) * 100,
            'RBLX_%': max_sharpe_weights_dict.get('RBLX', 0) * 100,
            'VWCE_DE_%': max_sharpe_weights_dict.get('VWCE_DE', 0) * 100,
            'Roblox_Total_%': roblox_weight_max,
            'Stocks_Total_%': stocks_weight_max
        }
    ])
    
    output_path = os.path.join(OUTPUT_DIR, "optimal_portfolios.csv")
    optimal_summary.to_csv(output_path, index=False)
    print(f"\n✅ Optimal portfolios saved to: {output_path}")
    
    efficient_frontier = pd.DataFrame({
        'Expected_Return_%': all_results[0] * 100,
        'Volatility_%': all_results[1] * 100,
        'Sharpe_Ratio': all_results[2]
    })
    
    ef_output_path = os.path.join(OUTPUT_DIR, "efficient_frontier.csv")
    efficient_frontier.to_csv(ef_output_path, index=False)
    print(f"✅ Efficient frontier data saved to: {ef_output_path}")
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE!")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()







    