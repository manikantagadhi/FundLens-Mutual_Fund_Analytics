# ⚙️ Scripts Directory: Automation & Applications

This directory shifts the project from static analysis to automated software engineering. It contains modular, standalone Python scripts.

## 📂 Directory Structure

```text
📦scripts
 ┣ 📜live_nav_fetch.py
 ┣ 📜recommender.py
 ┣ 📜send_email_report.py        # Automated Executive Email Script
 ┣ 📜scheduler.py                # Background Watchdog automation task
 ┣ 📜monte_carlo.py              # 5-Year Predictive Simulation Engine
 ┣ 📜portfolio_optimization.py   # Markowitz Efficient Frontier Engine
 ┗ 📜README.md
```

## 🚀 Application Details

### 1. live_nav_fetch.py (Automated API Extraction)

A robust data extraction script that interfaces with the public mfapi.in REST API.

**Function:** Dynamically fetches real-time NAV data for 6 critical benchmark funds.

**Features:** Includes error handling, JSON parsing, and automated saving directly into the `data/raw/` pipeline.

---

### 2. recommender.py (Robo-Advisor Simulation)

An interactive Command Line Interface (CLI) application that recommends mutual funds based on quantitative metrics.

**Algorithm:** Prompts the user for a Risk Appetite (Low/Moderate/High). It dynamically maps this input against standard risk categories, filters the dataset, and ranks the results using the pre-calculated Sharpe Ratio to guarantee optimal risk-adjusted returns.

---

### 3. send_email_report.py (Automated Executive Email Script)
An enterprise-grade reporting automation script.
* **Function:** Generates and securely transmits a weekly HTML performance snapshot via email.
* **Features:** Utilizes `smtplib` and `python-dotenv` for secure credential management. Embeds dynamic SQL-derived data tables and attaches cryptographic inline images (MIMEImage) for executive-level readability.

---

### 4. scheduler.py (Background Watchdog Automation)
A persistent background system monitor.
* **Function:** Automates the daily data ingestion pipeline.
* **Features:** Uses the `schedule` library to autonomously trigger `live_nav_fetch.py` at 8:00 PM exclusively on weekdays (bypassing market holidays). Designed for seamless integration with OS-level Task Schedulers.

---

### 5. monte_carlo.py (5-Year Predictive Simulation Engine)
An advanced predictive mathematical modeling script.
* **Function:** Forecasts potential future NAV trajectories over a 5-year horizon.
* **Features:** Executes 1,000 independent statistical simulations using `NumPy` based on historical daily volatility and mean returns. Extracts 5th, 50th, and 95th probability percentiles to plot distinct 'Uncertainty Bands' and exports the visual analysis to the `reports/` directory.

---

### 6. portfolio_optimization.py (Markowitz Efficient Frontier Engine)
A rigorous financial optimization algorithm based on Modern Portfolio Theory.
* **Function:** Calculates the optimal percentage allocation mix across top-performing funds to maximize returns while minimizing risk.
* **Features:** Applies `scipy.optimize` (SLSQP algorithm) to mathematically maximize the portfolio's Sharpe Ratio. Simulates 10,000 randomized asset configurations to plot the definitive Efficient Frontier curve.

---

## 💻 Usage Instructions

Navigate to the root directory of the project (`bluestock_mf_capstone/`) and execute the scripts using Python:

```bash
# 1. Fetch live NAV data manually
python scripts/live_nav_fetch.py

# 2. Launch the Robo-Advisor
python scripts/recommender.py

# 3. Send automated weekly email report (Ensure .env is configured)
python scripts/send_email_report.py

# 4. Start the Background Watchdog Scheduler
python scripts/scheduler.py

# 5. Run Monte Carlo Simulation
python scripts/monte_carlo.py

# 6. Run Portfolio Optimization
python scripts/portfolio_optimization.py