# 💾 Data Directory: The Central Data Lake

This directory functions as the central nervous system of the Bluestock Mutual Fund Analytics project. It manages the complete data lifecycle—from raw ingestion to cleaned staging and final analytical warehousing.

## 📂 Directory Structure

```text
📦data
 ┣ 📂raw
 ┃ ┣ 📜08_investor_transactions.csv ... (and other raw files)
 ┃ ┗ 📜125497_HDFC_TOP_100_live.csv ... (and other API fetched files)
 ┣ 📂processed
 ┃ ┣ 📜clean_nav_history.csv
 ┃ ┣ 📜clean_transaction.csv
 ┃ ┗ 📜clean_performance.csv
 ┣ 📂db
 ┃ ┗ 📜bluestock_mf.db
 ┗ 📜README.md
```

## 🏗️ Data Architecture & Pipeline

### raw/ (Data Ingestion Layer)

Contains the immutable source files. This includes historical static datasets provided by Bluestock (over 87K+ transaction rows) and live data dynamically extracted using the mfapi.in REST API.

### processed/ (Transformation Layer)

The output of our Pandas-driven ETL pipeline. Data here has undergone strict cleaning protocols: missing values forward-filled (ffill), datetime standardized, duplicate records purged, and data types optimized.

### db/ (Warehousing Layer)

Houses the bluestock_mf.db SQLite database. The processed data is loaded here into a highly structured Star Schema, ensuring extremely fast querying and seamless integration with BI tools.

> **Note:** Due to GitHub file size limits, exceptionally large raw datasets may be tracked using Git LFS or excluded via .gitignore.