import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco

def run_optimization():
    # 1. Path Setup
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, '..', 'data', 'db', 'bluestock_mf.db')
    report_path = os.path.join(BASE_DIR, '..', 'reports', 'efficient_frontier.png')

    print("📥 Fetching historical NAV data for Top 5 Funds...")
    
    # 2. Fetch Data for Top 5 Funds (Using Benchmark Schemes)
    amfi_codes = ['125497', '119551', '120503', '118632', '119092']
    fund_names = ['HDFC Top 100', 'SBI Bluechip', 'ICICI Bluechip', 'Nippon Large Cap', 'Axis Bluechip']
    
    conn = sqlite3.connect(db_path)
    # Get NAV data for these 5 funds
    query = f"SELECT nav_date, amfi_code, nav FROM fact_nav WHERE amfi_code IN ({','.join(amfi_codes)})"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Pivot data so each column is a fund and each row is a date
    df_pivot = df.pivot(index='nav_date', columns='amfi_code', values='nav')
    df_pivot.columns = fund_names # Rename columns for easy reading
    df_pivot.dropna(inplace=True)

    # 3. Calculate Daily Returns & Annualized Metrics
    returns = df_pivot.pct_change().dropna()
    mean_returns = returns.mean() * 252 # Annualized Return
    cov_matrix = returns.cov() * 252    # Annualized Covariance (Risk)

    num_assets = len(fund_names)
    risk_free_rate = 0.065 # Assuming 6.5% risk-free rate (e.g., FD)

    # 4. Helper Functions for Portfolio Math
    def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns * weights)
        std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        return std, returns

    # Function to minimize (Negative Sharpe Ratio)
    def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
        p_std, p_ret = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        return -(p_ret - risk_free_rate) / p_std

    # 5. Optimize the Portfolio using Scipy
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}) # Weights must sum to 1
    bounds = tuple((0.0, 1.0) for asset in range(num_assets)) # No short selling (weights between 0 and 1)
    
    # Give equal starting weights (20% each)
    init_guess = num_assets * [1. / num_assets,]

    print("Running Scipy Optimizer to maximize Sharpe Ratio...")
    optimal_result = sco.minimize(neg_sharpe_ratio, init_guess, args=args,
                                  method='SLSQP', bounds=bounds, constraints=constraints)

    opt_weights = optimal_result.x
    opt_std, opt_ret = portfolio_annualised_performance(opt_weights, mean_returns, cov_matrix)
    opt_sharpe = (opt_ret - risk_free_rate) / opt_std

    # Print Optimal Portfolio Mix
    print("\n OPTIMAL PORTFOLIO ALLOCATION (Maximum Sharpe Ratio):")
    for idx, name in enumerate(fund_names):
        print(f"   - {name}: {opt_weights[idx]*100:.2f}%")
    print(f"Expected Annual Return: {opt_ret*100:.2f}%")
    print(f"Expected Annual Volatility (Risk): {opt_std*100:.2f}%")
    print(f"Sharpe Ratio: {opt_sharpe:.2f}\n")

    # 6. Generate Random Portfolios for the Efficient Frontier Curve
    print("🎲 Generating 10,000 random portfolios for the Efficient Frontier...")
    num_portfolios = 10000
    results = np.zeros((3, num_portfolios))
    
    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        
        p_std, p_ret = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        results[0,i] = p_std
        results[1,i] = p_ret
        results[2,i] = (p_ret - risk_free_rate) / p_std # Sharpe Ratio

    # 7. Plotting the Efficient Frontier
    print("Plotting the Efficient Frontier Graph...")
    plt.figure(figsize=(12, 8))
    
    # Scatter plot of all random portfolios colored by Sharpe Ratio
    scatter = plt.scatter(results[0,:], results[1,:], c=results[2,:], cmap='viridis', marker='o', s=10, alpha=0.5)
    plt.colorbar(scatter, label='Sharpe Ratio')
    
    # Mark the Optimal Portfolio with a Red Star
    plt.scatter(opt_std, opt_ret, marker='*', color='r', s=400, label='Optimal Portfolio (Max Sharpe)')
    
    plt.title('Markowitz Efficient Frontier (Top 5 Mutual Funds)', fontsize=16, fontweight='bold')
    plt.xlabel('Annualized Volatility / Risk (Std. Deviation)', fontsize=12)
    plt.ylabel('Annualized Expected Return', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Save the plot
    plt.savefig(report_path, bbox_inches='tight', dpi=300)
    print(f"Success! Efficient Frontier Graph saved to: reports/efficient_frontier.png")

if __name__ == "__main__":
    run_optimization()