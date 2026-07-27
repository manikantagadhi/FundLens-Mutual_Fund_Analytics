import schedule
import time
import subprocess
import os
from datetime import datetime

def run_nav_pipeline():
    # Determine the absolute path of live_nav_fetch.py located in the same directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(BASE_DIR, 'live_nav_fetch.py')
    
    # Check if today is a weekday (Monday = 0, Friday = 4)
    # Skip execution on weekends (5 = Saturday, 6 = Sunday) as markets are closed
    today = datetime.now().weekday()
    if today < 5: 
        print(f"[{datetime.now()}] Triggering Automated NAV Fetch Engine...")
        try:
            # Execute live_nav_fetch.py
            subprocess.run(['python', script_path], check=True)
            print(f"[{datetime.now()}] Watchdog: Task executed successfully.")
        except Exception as e:
            print(f"[{datetime.now()}] Watchdog Error: Failed to execute script. Details: {e}")
    else:
        print(f"[{datetime.now()}] Weekend detected. Skipping NAV fetch as markets are closed.")

# Schedule the task to run every day at 8:00 PM (20:00)
schedule.every().day.at("20:00").do(run_nav_pipeline)

print("⏰ Watchdog Automated Scheduler is now ACTIVE and monitoring...")
print("This script will automatically fetch NAV every weekday at 8:00 PM.")

# Infinite loop to keep the script running in the background
while True:
    schedule.run_pending()
    time.sleep(60) # Check for pending scheduled tasks every 60 seconds