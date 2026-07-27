# 📓 Notebooks Directory: Analytics & Data Engineering

This directory contains the sequential Jupyter Notebooks that document the exact methodology, thought process, and Python code used to transform raw data into actionable financial intelligence.

## 📂 Directory Structure

```text
📦notebooks
 ┣ 📜01_data_ingestion.ipynb
 ┣ 📜02_data_cleaning.ipynb
 ┣ 📜03_EDA_Analysis.ipynb
 ┣ 📜04_Performance_Analytics.ipynb
 ┣ 📜05_Advanced_Analytics.ipynb
 ┗ 📜README.md
```

## 🔬 Execution Pipeline & Methodology

For reproducibility, notebooks must be executed sequentially:

### 01_data_ingestion.ipynb

Focuses on schema validation. It verifies 100% mapping accuracy between fund master codes and historical NAV records.

### 02_data_cleaning.ipynb

The core ETL engine. Applies Pandas logic for handling missing values during market holidays, fixing structural errors, and utilizing SQLAlchemy to populate the SQLite database.

### 03_EDA_Analysis.ipynb

Drives exploratory data analysis. Uses Seaborn and Plotly to generate correlation matrices, demographic distributions, and AUM growth heatmaps.

### 04_Performance_Analytics.ipynb

The quantitative finance module. Computes annualized volatility, CAGR, Sharpe Ratio, Sortino Ratio, and constructs the Custom Fund Scorecard using weighted multi-variable ranking.

### 05_Advanced_Analytics.ipynb

Tackles predictive and risk analytics. Computes Historical Value at Risk (VaR), analyzes Sector Concentration (HHI), and conducts Investor Cohort Analysis to flag high-churn probability.

## ⚙️ Prerequisites

Install the required Python packages before execution:

```bash
pip install pandas numpy matplotlib seaborn plotly scipy sqlalchemy
```