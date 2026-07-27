# 📚 Data Dictionary: Mutual Fund Analytics Platform

**Project:** Bluestock Fintech Capstone Project  
**Database:** `bluestock_mf.db` (SQLite)  
**Schema Type:** Star Schema

This data dictionary provides a comprehensive overview of the database schema, including tables, columns, data types, and business definitions for the Mutual Fund Analytics Platform.

---

## 1. Dimension Table: `dim_fund`
Stores static information and master details about the mutual fund schemes.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | TEXT | Primary Key | Unique 6-digit identifier assigned by AMFI for the scheme. |
| `fund_house` | TEXT | - | Name of the Asset Management Company (e.g., SBI Mutual Fund). |
| `scheme_name` | TEXT | - | Full official name of the mutual fund scheme. |
| `category` | TEXT | - | Broad asset class category (Equity, Debt, Hybrid). |
| `sub_category` | TEXT | - | Specific fund sub-category (Large Cap, Small Cap, Gilt, etc.). |
| `plan` | TEXT | - | Investment plan type (Regular or Direct). |
| `risk_category` | TEXT | - | SEBI-defined risk level (Low, Moderate, High, Very High). |

---

## 2. Dimension Table: `dim_date`
Stores date-related dimensions to allow time-series analysis and filtering.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `date_id` | DATE | Primary Key | Date in `YYYY-MM-DD` format. |
| `year` | INTEGER | - | Year component of the date. |
| `month` | INTEGER | - | Month component of the date (1-12). |
| `day` | INTEGER | - | Day component of the month (1-31). |
| `is_weekday` | BOOLEAN | - | `TRUE` if Monday to Friday, `FALSE` for weekends. |

---

## 3. Fact Table: `fact_nav`
Stores the daily historical Net Asset Value (NAV) for the mutual fund schemes.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER | Primary Key | Auto-incremented unique identifier for the record. |
| `amfi_code` | TEXT | Foreign Key | Maps to `dim_fund.amfi_code`. |
| `nav_date` | DATE | Foreign Key | Date of the NAV record. Maps to `dim_date.date_id`. |
| `nav` | REAL | - | The Net Asset Value of the fund on that specific date. |

---

## 4. Fact Table: `fact_transactions`
Records synthetic investor transactions (SIPs, Lumpsums, Redemptions) anchored to real geographic distributions.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `tx_id` | INTEGER | Primary Key | Auto-incremented unique transaction ID. |
| `investor_id` | TEXT | - | Unique identifier for the investor (e.g., INV003054). |
| `amfi_code` | TEXT | Foreign Key | Maps to the scheme invested in (`dim_fund.amfi_code`). |
| `transaction_date` | DATE | Foreign Key | The date the transaction occurred. |
| `transaction_type` | TEXT | - | Type of investment: `SIP`, `Lumpsum`, or `Redemption`. |
| `amount_inr` | REAL | - | Transaction amount in Indian Rupees (INR). |
| `kyc_status` | TEXT | - | Verification status of the investor (`Verified` or `Pending`). |

---

## 5. Fact Table: `fact_performance`
Stores aggregated performance and risk metrics calculated from historical NAV data.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | TEXT | Primary Key | Foreign Key mapping to `dim_fund.amfi_code`. |
| `return_1yr_pct` | REAL | - | 1-year absolute return percentage. |
| `return_3yr_pct` | REAL | - | 3-year Compound Annual Growth Rate (CAGR) percentage. |
| `return_5yr_pct` | REAL | - | 5-year Compound Annual Growth Rate (CAGR) percentage. |
| `sharpe_ratio` | REAL | - | Risk-adjusted return metric (Higher is better). |
| `expense_ratio_pct` | REAL | - | Annual management fee charged by the AMC (in percentage). |
| `is_anomaly` | BOOLEAN | - | `TRUE` if the fund exhibits negative Sharpe ratios (Risk flag). |

---

## 6. Fact Table: `fact_aum`
Tracks the quarterly Assets Under Management (AUM) growth for top fund houses.

| Column Name | Data Type | Key Type | Business Definition |
| :--- | :--- | :--- | :--- |
| `aum_id` | INTEGER | Primary Key | Auto-incremented unique ID. |
| `fund_house` | TEXT | - | Name of the Asset Management Company. |
| `quarter_date` | DATE | - | The end date of the reported financial quarter. |
| `aum_crore` | REAL | - | Total Assets Under Management in Crores (INR). |

---
*Note: All data sources represent publicly available information from AMFI India and mfapi.in, cleaned and processed via Python ETL pipelines.*