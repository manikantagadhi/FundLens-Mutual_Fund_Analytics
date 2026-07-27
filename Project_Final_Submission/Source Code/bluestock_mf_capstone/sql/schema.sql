-- 1. Dimension Table: Fund Details
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code TEXT PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    risk_category TEXT
);

-- 2. Dimension Table: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    is_weekday BOOLEAN
);

-- 3. Fact Table: NAV History (ഇതായിരുന്നു വിട്ടുപോയത്)
CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code TEXT,
    nav_date DATE,
    nav REAL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (nav_date) REFERENCES dim_date(date_id)
);

-- 4. Fact Table: Investor Transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT,
    amfi_code TEXT,
    transaction_date DATE,
    transaction_type TEXT,
    amount_inr REAL,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date_id)
);

-- 5. Fact Table: Scheme Performance
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code TEXT PRIMARY KEY,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    sharpe_ratio REAL,
    expense_ratio_pct REAL,
    is_anomaly BOOLEAN,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- 6. Fact Table: AUM
CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house TEXT,
    quarter_date DATE,
    aum_crore REAL
);