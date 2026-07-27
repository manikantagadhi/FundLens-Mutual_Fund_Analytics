"""
Master Execution Script
-----------------------
This script orchestrates the end-to-end execution of the Bluestock Mutual Fund 
Analytics pipeline.
"""

import os 
import subprocess

def run_python_script(script_path):
    """Executes a python script and handles the output."""
    print(f"Executing {script_path}...")
    try:
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        print(f"Success: {script_path} executed without errors. \n")
        # Print the output from the fetched script so we can see it working
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error in {script_path}:\n{e.stderr}\n")

def main():
    print("=" *60)
    print("BlueStock Mutual fund analytics pipeline")
    print("=" *60)
    
    Get the absolute path of the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Build the exact path to the live_nav_fetch.py script
    live_nav_script = os.path.join(base_dir, 'scripts', 'live_nav_fetch.py')
    
    if os.path.exists(live_nav_script):
        run_python_script(live_nav_script)
    else:
        print(f"Warning: {live_nav_script} not found. Skipping API fetch.")
        
    print("\n" + "=" *60)
    print("Notebook Execution Order")
    print("=" *60)
    print("Please execute the Jupyter Notebooks sequentially in the 'notebooks' directory:")
    print("  1. 01_data_ingestion.ipynb    (Data Quality & Validation)")
    print("  2. 02_data_cleaning.ipynb     (ETL & DB Loading)")
    print("  3. 03_EDA_Analysis.ipynb      (Exploratory Data Analysis)")
    print("  4. 04_Performance_Analytics.ipynb (Risk Metrics & Scorecards)")
    print("  5. 05_Advanced_Analytics.ipynb    (VaR, Cohort, HHI)")
    
    print("\n" + "=" * 60)
    print(" To run the Recommender System, use:")
    print(" python scripts/recommender.py")
    print("=" * 60)
    
if __name__ == "__main__":
    main()