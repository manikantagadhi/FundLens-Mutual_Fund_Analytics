
<div align="center">

# 📈 Bluestock Mutual Fund Analytics
### End-to-End Mutual Fund Analytics & Business Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white)
![PowerBI](https://img.shields.io/badge/PowerBI-Dashboard-yellow?style=for-the-badge&logo=powerbi&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-purple?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Portfolio-black?style=for-the-badge&logo=github&logoColor=white)
![Status](https://img.shields.io/badge/Project-Completed-success?style=for-the-badge&logo=checkmarx&logoColor=white)

<br>
<a href="https://bluestock-analytics-hashmil.streamlit.app/" target="_blank">
  <img src="https://img.shields.io/badge/Live%20App-View%20Streamlit%20Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live Streamlit Dashboard" />
</a>
<br>

---
</div>

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [🌐 Live Web Application (Bonus Task)](#-live-web-application-bonus-task)
- [🚀 Day 1: Data Ingestion, API Integration & Quality Validation](#-day-1-data-ingestion-api-integration--quality-validation)
- [🛠️ Day 2: Data Cleaning & SQL Database Design](#️-day-2-data-cleaning--sql-database-design)
- [📊 Day 3: Exploratory Data Analysis & Business Insights](#-day-3-exploratory-data-analysis--business-insights)
- [📈 Day 4: Fund Performance Analytics](#-day-4-fund-performance-analytics)
- [📊 Day 5: Dashboard Development (Power BI)](#-day-5-dashboard-development-power-bi)
- [🧠 Day 6: Advanced Analytics & Risk Metrics](#-day-6-advanced-analytics--risk-metrics)
- [🚀 Day 7: Pipeline Automation, Code Standardization & Final Submission](#-day-7-pipeline-automation-code-standardization--final-submission)
- [🌟 Day 8-9: Advanced Bonus Tasks & Enterprise Automation](#-day-8-9-advanced-bonus-tasks--enterprise-automation)
- [🏗️ System Architecture & Data Flow](#️-system-architecture--data-flow)
- [📊 Analytical Metrics Engine](#-analytical-metrics-engine)
- [🖥️ Interactive Dashboard Architecture](#️-interactive-dashboard-architecture)
- [📂 Repository Structure](#-repository-structure)
- [🛠️ Execution & Setup Guide](#️-execution--setup-guide)
- [📑 Final Deliverables](#-final-deliverables)
- [📜 License](#-license)

---

## 🎯 Project Overview

This repository contains the completed Capstone Project for the **Bluestock Fintech Data Analytics Internship**.

The goal of this project is to build an end-to-end Mutual Fund Analytics Platform using real-world public data from AMFI India and `mfapi.in`.

This README documents the progressive completion of daily milestones, moving from raw data ingestion to structured data engineering, analytics, dynamic Power BI Dashboards, advanced Python recommender systems, and final production automation.

**Phases Completed:** `Day 1` • `Day 2` • `Day 3` • `Day 4` • `Day 5` • `Day 6` • `Day 7` • `Day 8-9 (Bonus)`

**Status:** `Completed & Deployed`

---
## 🌐 Live Web Application (Bonus Task)

As an extra-mile initiative, the analytical engine has been deployed as a publicly accessible, interactive web application.

👉 **[Launch Bluestock Analytics Pro (Live App)](https://bluestock-analytics-hashmil.streamlit.app/)**

**Premium Features Integrated:**
* Institutional-grade dark-themed UI with custom glassmorphism CSS.
* Real-time Multi-Fund Relative Performance Tracking (Base 100 Indexing).
* 50-Day Simple Moving Average (SMA) Momentum Indicators.
* Dynamic SQLite Database connectivity with smart CSV fallbacks via Absolute Path Resolution.

---

## 🚀 Day 1: Data Ingestion, API Integration & Quality Validation

### 1. Project Architecture & Setup
- Initialized a standard data science folder structure (`data/raw`, `data/processed`, `notebooks`, `scripts`, `sql`, `dashboard`, `reports`).
- Set up a virtual environment and installed core dependencies listed in `requirements.txt` (Pandas, Requests, NumPy, etc.).

### 2. Static Data Ingestion
- Successfully loaded 10 extensive real-world CSV datasets provided by Bluestock (comprising 40 schemes, 4.5 years of NAV history, and 87K+ transaction rows).
- Evaluated dataset schemas, shapes, and data types to prepare for downstream transformation.

### 3. Live API Integration (Live NAV Fetcher)
- Developed an automated Python script (`scripts/live_nav_fetch.py`) to interact with the public `mfapi.in` REST API.
- Dynamically fetched live NAV data for 6 critical benchmark schemes:
  - *HDFC Top 100 Direct (125497)*
  - *SBI Bluechip (119551)*
  - *ICICI Bluechip (120503)*
  - *Nippon Large Cap (118632)*
  - *Axis Bluechip (119092)*
  - *Kotak Bluechip (120841)*

### 4. Initial Exploratory Data Analysis (EDA)
- Conducted preliminary exploration of the `01_fund_master.csv` dataset.
- Extracted and mapped unique Fund Houses, Categories, Sub-categories, and Risk Grades to understand the AMFI scheme code structure.

### 5. Data Quality & Validation
- Executed a strict validation protocol to ensure cross-dataset integrity.
- Confirmed a **100% match** by validating that every AMFI scheme code present in the `fund_master` dataset flawlessly aligns with the historical records in the `nav_history` dataset.

---

## 🛠️ Day 2: Data Cleaning & SQL Database Design

### 1. Data Cleaning Pipeline (Pandas)
- **NAV History:** Parsed dates, sorted records by scheme, removed duplicates, and implemented critical forward-filling (`ffill`) logic to handle missing NAV values during weekends and market holidays.
- **Transactions:** Standardized transaction types (SIP, Lumpsum, Redemption), validated positive investment amounts, fixed date formats, and filtered valid KYC statuses.
- **Scheme Performance:** Validated numeric return values, flagged risk anomalies (e.g., negative Sharpe ratios), and enforced acceptable expense ratio ranges.
- Exported all cleaned datasets to the `data/processed/` directory.

### 2. Database Schema Design
- Designed a professional analytical **Star Schema** with dimension tables (`dim_fund`, `dim_date`) and fact tables (`fact_nav`, `fact_transactions`, `fact_performance`, `fact_aum`).
- Authored strict DDL statements (`sql/schema.sql`) defining Primary Keys and Foreign Keys for data integrity.

### 3. Data Loading (SQLAlchemy)
- Created an automated Python pipeline using `SQLAlchemy` to generate a local SQLite database (`bluestock_mf.db`).
- Iteratively mapped, transformed, and loaded tens of thousands of processed records from Pandas DataFrames directly into the structured SQL tables.

### 4. Analytical SQL Queries
- Authored 10 business-critical SQL queries (`sql/queries.sql`) to extract insights such as:
  - Top 5 Fund Houses by AUM.
  - Average NAV trends per month.
  - Total SIP Amount by Year (YoY Growth).
  - Transaction volumes distributed by Fund Category.

### 5. Documentation
- Created a comprehensive Data Dictionary (`data_dictionary.md`) documenting all tables, columns, data types, and business logic to ensure project maintainability.

---

## 📊 Day 3: Exploratory Data Analysis & Business Insights

### 1. Time-Series Analysis
- Plotted the daily NAV trend for 40 schemes (2022-2026), successfully highlighting the 2023 bull run and 2024 market corrections using `Plotly`.
- Visualized monthly SIP inflow trends, dynamically annotating the all-time high of ₹31,002 Cr.
- Charted the mutual fund industry's folio count growth showing an increase from 13.26 Cr to 26.12 Cr.

### 2. Market Size & Category Analysis
- Developed grouped bar charts to analyze AUM growth by fund house, highlighting SBI's dominance (~12.5L Cr).
- Created a Seaborn heatmap to track net inflow intensity across different fund categories over time.
- Built a sector allocation donut chart showing heavy investments in the Banking, IT, and Pharma sectors.

### 3. Investor Demographics
- Analyzed the investor base using interactive pie charts to show age group distribution (majority 26-35) and gender split.
- Designed box plots to observe SIP ticket size distribution across different age groups.
- Mapped geographic distribution with horizontal bar charts for state-wise SIP contributions and a T30 vs B30 city tier breakdown.

### 4. Fund Performance Correlation
- Computed a pairwise correlation matrix of daily returns for 10 selected funds and visualized it using a Seaborn heatmap to understand scheme dependencies and market movement similarities.

### 5. Insights & Deliverables
- Documented **10 key EDA findings** bridging data visualizations with actionable business insights directly within the Jupyter Notebook (`03_EDA_Analysis.ipynb`).
- Exported 15+ interactive and static charts to the `reports/` directory for final presentation preparation.

---

## 📈 Day 4: Fund Performance Analytics

### 1. Return Calculations
- Computed **Daily Returns** for all 40 schemes and validated the normal distribution of returns.
- Calculated the **Compound Annual Growth Rate (CAGR)** for 1-Year, 3-Year, and 5-Year horizons.

### 2. Risk Metrics
- Calculated annualized return and volatility metrics.
- Computed the **Sharpe Ratio** (using a 6.5% risk-free rate) to measure risk-adjusted returns.
- Computed the **Sortino Ratio** focusing solely on downside risk.
- Identified the **Maximum Drawdown (MDD)** for each fund to assess maximum historical loss.

### 3. Alpha & Beta (Market Regression)
- Utilized `scipy.stats.linregress` to perform an OLS regression of fund returns against the market benchmark.
- Extracted annualized **Alpha** (excess return over market) and **Beta** (market volatility correlation).

### 4. Composite Fund Scorecard
- Built a robust 0-100 Fund Scorecard system by applying strategic weights:
  - 30% for 3Y CAGR
  - 25% for Sharpe Ratio
  - 20% for Alpha
  - 15% for Expense Ratio (Inverse)
  - 10% for Max Drawdown (Inverse)
- Ranked and identified the Top 10 mutual funds in the dataset based on this composite score.

### 5. Benchmark Comparison & Tracking Error
- Visualized the Top 5 best-performing funds against the Market Benchmark over a 3-year cumulative growth period.
- Computed the **Tracking Error** to measure how closely the funds follow the benchmark index.
- Exported analytical results (`alpha_beta.csv`, `fund_scorecard.csv`) and visualizations (`benchmark_comparison.png`) to the `reports/` directory.

---

## 📊 Day 5: Dashboard Development (Power BI)

### 1. Data Modeling & Connection
- Imported processed CSV files and benchmark indices into Power BI to construct a comprehensive, interactive data model.

### 2. Page 1: Industry Overview
- Designed dynamic KPI cards highlighting Total AUM (₹81L Cr), Monthly SIP Inflows (₹31K Cr), and Industry Folios (26.12 Cr).
- Visualized historical AUM growth trends and top 10 dominant fund houses.

### 3. Page 2: Fund Performance
- Built an interactive Risk vs. Reward scatter plot (Return vs. Volatility).
- Integrated the custom 0-100 Fund Scorecard as a sortable matrix.
- Created comparative NAV line charts with drill-through capabilities.

### 4. Page 3: Investor Analytics
- Visualized demographic insights including transaction volume by state and age-group SIP averages.
- Developed a Donut chart comparing SIP, Lumpsum, and Redemption distributions.

### 5. Page 4: SIP & Market Trends
- Developed a dual-axis chart correlating monthly SIP inflows with the Nifty 50 index movement.
- Built a Matrix Heatmap to track category-wise capital inflows over time.
- Implemented Top N filtering to showcase the most invested fund categories in FY25.

### 6. Deliverables
- Exported the finalized, branded dashboard as `bluestock_mf_dashboard.pbix`.
- Generated a comprehensive multi-page `Dashboard.pdf` and high-resolution PNG snapshots for final reporting.

---

## 🧠 Day 6: Advanced Analytics & Risk Metrics

### 1. Advanced Risk Metrics (VaR & CVaR)
- Computed **Historical Value at Risk (VaR)** at a 95% confidence interval to determine the maximum expected daily loss for each fund.
- Calculated **Conditional VaR (CVaR)** to measure the average loss in worst-case scenarios.
- Visualized the **90-Day Rolling Sharpe Ratio** for top 5 funds to observe dynamic changes in risk-adjusted returns over time.

### 2. Investor Behavioral Analytics
- **Cohort Analysis:** Grouped investors by their first transaction year (2024 vs. 2025). Discovered that while 2024 had higher total investments, the 2025 cohort showed a higher average SIP amount (₹13,505 vs ₹10,996).
- **SIP Continuation Risk:** Analyzed transaction gaps for investors with 6+ SIPs. Successfully flagged investors with average gaps exceeding 35 days as 'at-risk' for potential churn.

### 3. Sector Concentration Risk (HHI)
- Applied the **Herfindahl-Hirschman Index (HHI)** on portfolio holdings to assess sector concentration.
- Identified and visualized the Top 10 most concentrated (high-risk) funds, highlighting vulnerabilities to specific sector downturns.

### 4. Fund Recommendation System
- Built an interactive Python script (`scripts/recommender.py`) to simulate a robo-advisor.
- The system takes user **Risk Appetite (Low / Moderate / High)** as input and dynamically recommends the Top 3 mutual funds utilizing the Sharpe Ratio and matching risk grades.

---

## 🚀 Day 7: Pipeline Automation, Code Standardization & Final Submission

### 1. Master Pipeline Orchestration (`run_pipeline.py`)
- Engineered a centralized execution master controller script (`run_pipeline.py`) located at the project root folder.
- Utilizes dynamic workspace **Absolute Path Resolution** (`os.path.abspath(__file__)`) to reliably map and run the dynamic data ingestion sequence irrespective of the user's execution terminal environment.
- Implemented professional subprocess handling using `subprocess.run` with strict `CalledProcessError` exceptions to isolate syntax or network latency bottlenecks during real-time extraction.

### 2. Repository Cleaning & Modular Subdirectory Documentation
- Standardized directory hygiene by reviewing, structuring, and deploying custom, standalone `README.md` descriptive files across all 6 submodules (`data/`, `notebooks/`, `scripts/`, `sql/`, `dashboard/`, `reports/`).
- Clarified downstream asset visibility including Star Schema environments, Power BI structures, specific quantitative `.csv` results, and execution orders.

### 3. Production of Final Executive Deliverables
- Compiled and formatted the **Comprehensive Final Report** (`Final_Report.pdf`, `Final_Report.docx`) in the `reports/` folder, neatly detailing Executive Summaries, Star Schema performance, advanced risk matrices, and Power BI navigation logs.
- Produced the comprehensive **12-Slide Presentation Deck** (`Bluestock_MF_Presentation.pptx`) utilizing an optimized fintech visual palette layout to effectively pitch strategic business discoveries and automated risk rebalancing methodologies to core stakeholders.

---

## 🌟 Day 8-9: Advanced Bonus Tasks & Enterprise Automation

### 1. Automated Business Intelligence Reporting (`send_email_report.py`)
- Developed a secure Python script integrating `smtplib` and `email.mime` for automated weekly performance report generation.
- Configured dynamic HTML template embedding SQLite-derived tables and inline cryptographic images (MIMEImage) for executive delivery.
- Implemented `.env` credential management via `python-dotenv` to ensure secure pipeline integrations without exposing application passwords.

### 2. Background Watchdog Scheduler (`scheduler.py`)
- Engineered a persistent system "Watchdog" utilizing the `schedule` library to automate the `live_nav_fetch.py` pipeline.
- Designed with intelligent datetime logic to execute exclusively on weekdays at 8:00 PM, bypassing weekends to align with market hours. 
- Integrated seamlessly with OS-level Task Schedulers (Windows Task Scheduler) for uninterrupted background execution on boot.

### 3. Monte Carlo Simulation Engine (`monte_carlo.py`)
- Engineered a predictive mathematical model using NumPy to forecast 5-year future Net Asset Value (NAV) trajectories.
- Executed 1,000 independent statistical simulations based on historical volatility and return metrics.
- Visualized 'Uncertainty Bands' extracting 5th, 50th, and 95th probability percentiles to map risk-adjusted market outcomes and exported the analysis to the `reports/` directory.

### 4. Portfolio Optimization Engine (`portfolio_optimization.py`)
- Deployed a portfolio optimization algorithm based on Modern Portfolio Theory (Markowitz Efficient Frontier).
- Utilized `scipy.optimize` to mathematically maximize the Sharpe Ratio and deduce the optimal percentage allocation mix across top-performing funds.
- Simulated 10,000 distinct portfolio configurations to visualize the risk-reward tradeoff spectrum, plotting the ultimate Efficient Frontier curve for institutional reporting.

### 5. Interactive Live Web Application (`streamlit_app.py`)
- Engineered a full-stack, publicly accessible mutual fund analytics dashboard using Streamlit.
- Implemented institutional-grade dark-themed UI, custom glassmorphism CSS, and real-time Multi-Fund Relative Performance Tracking (Base 100 Indexing).
- Successfully deployed the application to Streamlit Community Cloud with dynamic SQLite Database connectivity and smart CSV fallbacks via Absolute Path Resolution.

---

## 🏗️ System Architecture & Data Flow

```text
            ┌───────────────────────────────────────┐
[Raw AMFI Ingestion Layer]               [Dynamic Live REST API]
            │                                       │
            ▼                                       ▼
   (Pandas Data Cleaning)              (scripts/live_nav_fetch.py)
            │                                       │
            └───────────────────┬───────────────────┘
                                │
                                ▼
                    [SQLAlchemy ETL Engine]
                                │
                                ▼
         [Structured Star Schema Warehouse: SQLite DB]

          ┌────────────────────────────────────────────┐
          │ Dimensions : dim_fund, dim_date, dim_user  │
          │ Facts      : fact_nav, fact_transactions,  │
          │              fact_performance              │
          └─────────────────────┬──────────────────────┘
                                │
          ┌─────────────────────┼───────────────────────┐
          ▼                     ▼                       ▼

[Jupyter Analytics]    [Power BI BI Engine]        [Robo Recommender App]
📊 Advanced Risk(VaR)  📊 Multi-page Dashboards   ⚙️Sharpe-driven Risk
📊 Concentration(HHI)  📊 Drill-through Insights   Mapping CLI Tool
```

---

## 📊 Analytical Metrics Engine

| Metric Layer | Statistical Implementation | Operational Purpose |
|--------------|---------------------------|---------------------|
| **CAGR** | (End Value / Start Value)^(1/n) - 1 | Compounded annualized growth rate evaluation |
| **Sharpe Ratio** | (Rp - Rf) / σp | Reward-to-volatility performance measurement |
| **Alpha & Beta** | Rp = α + βRm + ε | Market benchmark regression analysis |
| **Value at Risk (VaR)** | 5th Percentile (Historical Distribution) | Captures extreme downside risk exposure |
| **HHI Index** | Σ(Si²) | Measures sector concentration risk |

> **Note:** GitHub Markdown does not natively render LaTeX equations inside tables. Formula notation has been simplified for proper display.

---

## 🖥️ Interactive Dashboard Architecture

The Power BI visualization layout contains four strategic analytic portals engineered for executive stakeholders:

* **Industry Overview (Portal 1):** Real-time monitoring matrix evaluating macro KPIs, underlying growth curves, and market share distribution maps across dominant asset management houses.
* **Fund Performance Matrix (Portal 2):** Advanced portfolio tracking layout featuring interactive scatter visuals alongside custom 0-100 composite index matrixes.
* **Investor Behavioral Trends (Portal 3):** Demographic profiling tracking regional volume distribution, city tiers, and redemption flow metrics.
* **Market Inflow Dynamics (Portal 4):** Dual-axis tracking environments correlating underlying mutual fund growth lines with structural financial market indicators over time.

---

## 📁 Repository Structure

```text
📦bluestock_mf_capstone
 ┣ 📂data
 ┃ ┣ 📂raw                         # Immutable source assets & live API extractions
 ┃ ┃ ┣ 📜01_fund_master.csv
 ┃ ┃ ┣ 📜02_nav_history.csv
 ┃ ┃ ┣ 📜... (Other raw datasets)
 ┃ ┃ ┗ 📜125497_HDFC_TOP_100_live.csv
 ┃ ┣ 📂processed                   # Standardized, cleaned, and filled datasets
 ┃ ┃ ┣ 📜clean_nav_history.csv
 ┃ ┃ ┗ 📜clean_transaction.csv
 ┃ ┣ 📂db                          # SQLite Star Schema warehouse engine
 ┃ ┃ ┗ 📜bluestock_mf.db
 ┃ ┗ 📜README.md
 ┣ 📂notebooks                     # Sequential pipeline processing environments
 ┃ ┣ 📜01_data_ingestion.ipynb
 ┃ ┣ 📜02_data_cleaning.ipynb
 ┃ ┣ 📜03_EDA_Analysis.ipynb
 ┃ ┣ 📜04_Performance_Analytics.ipynb
 ┃ ┣ 📜05_Advanced_Analytics.ipynb
 ┃ ┗ 📜README.md
 ┣ 📂scripts                       # Production automation & execution apps
 ┃ ┣ 📜live_nav_fetch.py
 ┃ ┣ 📜recommender.py
 ┃ ┣ 📜send_email_report.py        # Automated Executive Email Script
 ┃ ┣ 📜scheduler.py                # Background Watchdog automation task
 ┃ ┣ 📜monte_carlo.py              # 5-Year Predictive Simulation Engine
 ┃ ┣ 📜portfolio_optimization.py   # Markowitz Efficient Frontier Engine
 ┃ ┗ 📜README.md
 ┣ 📂sql                           # Structural warehouse creation logic
 ┃ ┣ 📜schema.sql
 ┃ ┣ 📜queries.sql
 ┃ ┗ 📜README.md
 ┣ 📂dashboard                     # Front-end business intelligence binaries
 ┃ ┣ 📜bluestock_mf_dashboard.pbix
 ┃ ┗ 📜README.md
 ┣ 📂reports                       # Exported analytical metrics, visuals & PDFs
 ┃ ┣ 📜*.png (14+ EDA, Dashboard & Adv. Analytics visuals)
 ┃ ┣ 📜*.csv (Scorecards, VaR, HHI, Cohort & Optimization Data)
 ┃ ┣ 📜Dashboard Export.pdf
 ┃ ┣ 📜Final_Report.pdf/docx
 ┃ ┗ 📜README.md
 ┣ 📜streamlit_app.py              # Premium Streamlit Web Dashboard
 ┣ 📜requirements.txt              # Standard system dependencies
 ┣ 📜data_dictionary.md            # Warehouse data model catalog
 ┣ 📜run_pipeline.py               # Absolute path automation master controller
 ┗ 📜Bluestock_MF_Presentation.pptx # Fintech investment presentation deck

```

---

## 🛠️ Execution & Setup Guide

### 1. System Deployment & Virtual Environment Setup

Initialize a shell platform inside your target workstation path, fetch the production repository, and activate the Python dependency environment:

```bash
# Clone the repository
git clone https://github.com/Hashmil-Muhammed/Bluestock-Data-Analyst-Internship/tree/main/bluestock_mf_capstone

cd bluestock_mf_capstone

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Automation Master Pipeline

Execute the root orchestration file. This handles dynamic absolute directory discovery, ensures structural alignment, and triggers live REST API endpoints automatically:

```bash
python run_pipeline.py
```

### 3. Initialize the Interactive Financial Robo-Advisor App

Launch the interactive terminal-based tool to evaluate mutual fund schemes dynamically against individual risk parameters:

```bash
python scripts/recommender.py
```

### 4. Review Analytical Environments & Visual Dashboards

- Navigate into the `notebooks/` workspace and execute files `01` through `05` sequentially.
- Open `dashboard/bluestock_mf_dashboard.pbix` using Power BI Desktop to explore interactive visualizations and performance insights.

---

## 📑 Final Deliverables

### Project Deliverables

- 📄 `Bluestock_MF_Capstone_Project.pdf`
- 📊 `Bluestock_MF_Presentation.pptx`
- 📈 `bluestock_mf_dashboard.pbix`
- 📑 `Final_Report.pdf`
- 🗄️ `bluestock_mf.db`
- 📋 `fund_scorecard.csv`
- 📋 `alpha_beta.csv`
- 📋 `var_cvar_reports.csv`
- 📋 `sector_hhi.csv`
- 📋 `cohort_analysis.csv`

---

## 📜 License

This project was developed as part of the **Bluestock Fintech Data Analytics Internship Capstone Project** and is intended for educational and portfolio purposes.