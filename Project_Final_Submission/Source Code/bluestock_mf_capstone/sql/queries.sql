-- 1. Top 5 Fund Houses by AUM (Latest Data)
SELECT fund_house, MAX(quarter_date) AS latest_quarter, aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT strftime('%Y-%m', nav_date) AS month, ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY month
ORDER BY month;

-- 3. Total SIP Amount by Year (SIP YoY Growth proxy)
SELECT strftime('%Y', transaction_date) AS year, SUM(amount_inr) AS total_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year;

-- 4. Transactions Volume by Fund Category
SELECT f.category, COUNT(t.tx_id) AS total_transactions, SUM(t.amount_inr) AS total_volume
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
GROUP BY f.category
ORDER BY total_volume DESC;

-- 5. Funds with Expense Ratio < 1%
SELECT f.scheme_name, f.fund_house, p.expense_ratio_pct
FROM dim_fund f
JOIN fact_performance p ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio_pct < 1.0
ORDER BY p.expense_ratio_pct ASC;

-- 6. Top 5 Best Performing Funds (Based on 3-year returns)
SELECT f.scheme_name, p.return_3yr_pct
FROM dim_fund f
JOIN fact_performance p ON p.amfi_code = f.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 5;

-- 7. Total Number of Schemes by Risk Category
SELECT risk_category, COUNT(amfi_code) AS number_of_schemes
FROM dim_fund
GROUP BY risk_category
ORDER BY number_of_schemes DESC;

-- 8. Total Amount Invested by Transaction Type (SIP vs Lumpsum)
SELECT transaction_type, SUM(amount_inr) AS total_amount, COUNT(tx_id) AS txn_count
FROM fact_transactions
GROUP BY transaction_type;

-- 9. Average Expense Ratio by Fund Category
SELECT f.category, ROUND(AVG(p.expense_ratio_pct), 2) AS avg_expense_ratio
FROM dim_fund f
JOIN fact_performance p ON p.amfi_code = f.amfi_code
GROUP BY f.category;

-- 10. List of Funds with Negative Sharpe Ratio (Risk Anomalies)
SELECT f.scheme_name, p.sharpe_ratio
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE p.sharpe_ratio < 0
ORDER BY p.sharpe_ratio ASC;

