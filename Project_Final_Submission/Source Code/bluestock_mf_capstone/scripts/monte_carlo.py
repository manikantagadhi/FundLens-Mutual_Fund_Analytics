import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_monte_carlo():
    # 1. Path Setup (Absolute Paths to prevent errors)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, '..', 'data', 'db', 'bluestock_mf.db')
    report_path = os.path.join(BASE_DIR, '..', 'reports', 'monte_carlo_projection.png')

    # 2. Fetch Historical Data (Using HDFC Top 100 as an example)
    print("Fetching historical NAV data...")
    conn = sqlite3.connect(db_path)
    query = "SELECT nav_date, nav FROM fact_nav WHERE amfi_code = '125497' ORDER BY nav_date"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # 3. Calculate Daily Returns & Statistical Variables
    df['returns'] = df['nav'].pct_change()
    df.dropna(inplace=True)

    mu = df['returns'].mean() # Average daily return
    sigma = df['returns'].std() # Daily volatility (Risk)
    last_nav = df['nav'].iloc[-1]

    # 4. Monte Carlo Simulation Setup
    simulations = 1000
    years = 5
    trading_days = 252 * years 

    print(f" Running {simulations} simulations for the next {years} years...")
    
    # Generate random normal returns
    random_returns = np.random.normal(loc=mu, scale=sigma, size=(trading_days, simulations))

    # Calculate price paths using Cumulative Product
    price_paths = np.zeros_like(random_returns)
    price_paths[0] = last_nav
    for t in range(1, trading_days):
        price_paths[t] = price_paths[t-1] * (1 + random_returns[t])

    # 5. Calculate Confidence Intervals (Uncertainty Bands)
    percentile_5 = np.percentile(price_paths, 5, axis=1)   # Pessimistic Scenario (Worst 5%)
    percentile_50 = np.percentile(price_paths, 50, axis=1) # Median Expected Scenario
    percentile_95 = np.percentile(price_paths, 95, axis=1) # Optimistic Scenario (Top 5%)

    # 6. Plotting the Data
    print("Generating Probability Graph...")
    plt.figure(figsize=(14, 7))
    
    # Plotting a sample of 100 random paths for visual effect
    plt.plot(price_paths[:, :100], color='#38bdf8', alpha=0.05) 

    # Plotting the Confidence Bands
    plt.plot(percentile_50, color='#facc15', linewidth=2.5, label='Expected Median NAV (50th Percentile)')
    plt.plot(percentile_95, color='#10b981', linewidth=2.5, linestyle='--', label='Optimistic Bound (95th Percentile)')
    plt.plot(percentile_5, color='#ef4444', linewidth=2.5, linestyle='--', label='Pessimistic Bound (5th Percentile)')

    plt.title('Monte Carlo Simulation: 5-Year Probability Forecast (HDFC Top 100)', fontsize=14, fontweight='bold')
    plt.xlabel('Future Trading Days (1 Year = 252 Days)', fontsize=12)
    plt.ylabel('Projected Net Asset Value (₹)', fontsize=12)
    plt.legend(loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Clean background for reports
    plt.gca().set_facecolor('#f8fafc')

    # 7. Save to Reports folder
    plt.savefig(report_path, bbox_inches='tight', dpi=300)
    print(f"Success! Graph saved to: reports/monte_carlo_projection.png")

if __name__ == "__main__":
    run_monte_carlo()