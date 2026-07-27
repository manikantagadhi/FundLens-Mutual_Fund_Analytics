"""
Live NAV Fetcher
----------------
This script interacts with the public mfapi.in REST API to dynamically fetch 
live Net Asset Value (NAV) data for critical benchmark mutual fund schemes.
"""

import requests
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

output_folder = 'G:\\My Drive\\WorkSpace\\Bluestock_Fintech_Data_Analyst_Intern\\Intership at BlueStock\\bluestock_mf_capstone\\data\\raw'
    
os.makedirs(output_folder, exist_ok=True)

funds = {
    "HDFC_TOP_100" : "125497",
    "SBI_Bluechip" : "119551",
    "ICICI_Bluechip" : "120503",
    "Nippom_Large_Cap" : "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip" : "120841",
}

print("Fetching live NAV data from mfapi.in...\n" + "-"*50)

for name, code in funds.items():
    url = f"https://api.mfapi.in/mf/{code}"
    print(f"Fetching : {name} (code: {code})...")
    
    try:
        response =requests.get(url)
        if response.status_code == 200:
            data = response.json()
            nav_data = data.get("data", [])
                
            if nav_data:
                df = pd.DataFrame(nav_data)
                    
                    
                files_path = os.path.join(output_folder, f"{code}_{name}_live.csv")
                df.to_csv(files_path, index=False)
                print(f" Saved Successfully to {files_path}")
            else:
                print(f"No NAV data found for {name}")
        else:
            print(f"Failed to fetch {name}. Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error While fetching {name}: {e}")
print("-" * 50 + "\nAll live data Fetching completed!")