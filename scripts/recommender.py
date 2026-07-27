"""
Mutual Fund Recommender System
------------------------------
This script recommends the top 3 mutual funds based on the user's risk appetite.
It merges fund master data with computed risk metrics (Sharpe Ratio) to provide
data-driven recommendations.
"""

import pandas as pd
import os

def recommend_funds(risk_appetite):
    """
    Recommends top 3 mutual funds based on the investor's risk appetite.
    Uses Sharpe Ratio to find the best risk-adjusted performers.
    """
    print(f"\nSearching for the best funds matching '{risk_appetite}' risk profile...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    
    # 1. Define file paths 
    master_path = os.path.join(base_dir, 'data', 'raw', '01_fund_master.csv')
    scorecard_path = os.path.join(base_dir, 'reports', 'fund_scorecard.csv')
    
    if not os.path.exists(master_path) or not os.path.exists(scorecard_path):
        print(f"Error: Required data files not found.\nPath 1: {master_path}\nPath 2: {scorecard_path}")
        return
    
    # 2. Load the data
    fund_master = pd.read_csv(master_path)
    fund_scores = pd.read_csv(scorecard_path)
    
    # BULLETPROOF FIX: Convert all column names to lowercase and replace spaces with underscores
    fund_master.columns = fund_master.columns.str.strip().str.lower().str.replace(' ', '_')
    fund_scores.columns = fund_scores.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Find the common column dynamically
    common_col = 'scheme_name' if 'scheme_name' in fund_scores.columns else 'amfi_code'
    if common_col not in fund_master.columns:
        print(f"Error: '{common_col}' not found in fund_master. Columns are: {fund_master.columns.tolist()}")
        return
        
    # Find risk column dynamically
    risk_col = 'risk_grade'
    for col in fund_master.columns:
        if 'risk' in col:
            risk_col = col
            break
            
    # 3. Merge data 
    merged_data = pd.merge(fund_scores, fund_master[[common_col, risk_col]], on=common_col, how='inner')
    
    risk_appetite = risk_appetite.strip().title()
    
    if risk_appetite == 'Low':
        target_grades = ['Low', 'Low To Moderate']
    elif risk_appetite == 'Moderate':
        target_grades = ['Moderate', 'Moderately High']
    elif risk_appetite == 'High':
        target_grades = ['High', 'Very High']
    else:
        print("Invalid input! Please choose exactly from: Low, Moderate, High.")
        return
    
    # Standardize data values to Title Case to ensure perfect match
    merged_data[risk_col] = merged_data[risk_col].astype(str).str.strip().str.title()
    
    # 4. Filter funds
    filtered_funds = merged_data[merged_data[risk_col].isin(target_grades)]
    
    if filtered_funds.empty:
        print(f"No matching funds for risk profile: {risk_appetite}")
        return
    
    # Find Sharpe Ratio column dynamically
    sharpe_col = 'sharpe_ratio'
    for col in filtered_funds.columns:
        if 'sharpe' in col:
            sharpe_col = col
            break
            
    # 5. Sort by Sharpe Ratio
    top_3_funds = filtered_funds.sort_values(by=sharpe_col, ascending=False).head(3)
    
    # 6. Print the recommendation table
    print(f"\n Top 3 Recommended Funds ({risk_appetite} Risk):")
    print("-" * 80)
    
    display_cols = [common_col, risk_col, sharpe_col]
    
    # Find CAGR column safely
    for col in filtered_funds.columns:
        if 'cagr' in col:
            display_cols.append(col)
            break
            
    print(top_3_funds[display_cols].to_string(index=False))
    print("-" * 80)
    print("Recommendation based on maximum risk-adjusted returns (Sharpe Ratio).")

if __name__ == "__main__":
    print("=" * 50)
    print("Bluestock Mutual Fund Recommender System")
    print("=" * 50)
    
    user_risk = input("Enter your risk appetite (Options: Low / Moderate / High): ")
    recommend_funds(user_risk)
