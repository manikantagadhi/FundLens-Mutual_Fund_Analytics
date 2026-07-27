# 🗄️ SQL Directory: Analytical Data Warehousing

This directory contains the database engineering scripts. By moving from flat CSV files to a structured relational database, the project achieves enterprise-level querying efficiency.

## 📂 Directory Structure

```text
📦sql
 ┣ 📜schema.sql
 ┣ 📜queries.sql
 ┗ 📜README.md
```

## 🏗️ Architecture & Usage

### 1. Data Definition (schema.sql)

Defines the architectural backbone of the bluestock_mf.db database using a Star Schema approach optimized for OLAP (Online Analytical Processing).

**Dimension Tables:**

- dim_fund
- dim_date
- dim_investor

**Fact Tables:**

- fact_nav
- fact_transactions
- fact_performance

Ensures data integrity through strict Primary Key and Foreign Key constraints.

---

### 2. Data Manipulation & Extraction (queries.sql)

A suite of business-critical analytical queries utilizing advanced SQL functions (CTEs, Window Functions, JOINs, Aggregations).

#### Examples of insights generated:

- Year-over-Year (YoY) SIP investment growth.
- Top 5 AMCs by total Asset Under Management (AUM).
- Transaction volume distribution across various fund categories.