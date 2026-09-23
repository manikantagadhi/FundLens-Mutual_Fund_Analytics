import os
import sqlite3
import pandas as pd
import numpy as np

from scripts.risk_engine import calculate_risk_metrics
from scripts.fund_health_score import calculate_fund_health_score
from scripts.fund_comparison import compare_fund
from scripts.monte_carlo import run_monte_carlo
from scripts.portfolio_engine import (
    calculate_returns_matrix,
    calculate_portfolio_metrics,
    calculate_diversification_score
)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "db",
    "bluestock_mf.db"
)


print("=" * 60)
print("FundLens V2 - Validation Test")
print("=" * 60)


# ============================================================
# 1. LOAD DATA
# ============================================================

print("\n[1/5] Loading database...")

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    n.nav_date,
    n.nav,
    n.amfi_code,
    f.scheme_name,
    f.category
FROM fact_nav n
JOIN dim_fund f
    ON n.amfi_code = f.amfi_code
"""

df_nav = pd.read_sql_query(
    query,
    conn
)

conn.close()

df_nav["nav_date"] = pd.to_datetime(
    df_nav["nav_date"]
)

print(
    f"Loaded {len(df_nav):,} NAV records"
)

print(
    f"Found {df_nav['scheme_name'].nunique()} funds"
)


# ============================================================
# 2. RISK ENGINE
# ============================================================

print("\n[2/5] Testing Risk Engine...")

fund_name = (
    df_nav["scheme_name"]
    .value_counts()
    .index[0]
)

fund_data = (
    df_nav[
        df_nav["scheme_name"] == fund_name
    ]
    .sort_values("nav_date")
)

risk_metrics = calculate_risk_metrics(
    fund_data["nav"]
)

required_metrics = [
    "annualized_return",
    "volatility",
    "sharpe_ratio",
    "sortino_ratio",
    "max_drawdown",
    "var_95",
    "cvar_95"
]

for metric in required_metrics:

    assert metric in risk_metrics, (
        f"Missing risk metric: {metric}"
    )

print("✓ Risk Engine passed")


# ============================================================
# 3. FUND HEALTH SCORE
# ============================================================

print("\n[3/5] Testing Fund Health Score...")

health_score = calculate_fund_health_score(
    risk_metrics
)

assert 0 <= health_score <= 100

print(
    f"✓ Health Score passed: "
    f"{health_score:.2f}/100"
)

assert 0 <= health_score <= 100

print(
    f"✓ Health Score passed: "
    f"{health_score:.2f}/100"
)


# ============================================================
# 4. MONTE CARLO
# ============================================================

print("\n[4/5] Testing Monte Carlo...")

mc_result = run_monte_carlo(
    fund_data["nav"],
    initial_investment=100000,
    years=1,
    simulations=100
)

assert len(
    mc_result["final_values"]
) == 100

assert (
    mc_result["median_final_value"]
    if "median_final_value" in mc_result
    else mc_result["summary"]["median_final_value"]
)

print(
    "✓ Monte Carlo Engine passed"
)


# ============================================================
# 5. PORTFOLIO ENGINE
# ============================================================

print("\n[5/5] Testing Portfolio Engine...")

top_funds = (
    df_nav["scheme_name"]
    .value_counts()
    .head(3)
    .index
    .tolist()
)

portfolio_data = df_nav[
    df_nav["scheme_name"].isin(
        top_funds
    )
][
    [
        "scheme_name",
        "nav_date",
        "nav"
    ]
].copy()

returns_matrix = calculate_returns_matrix(
    portfolio_data
)

returns_matrix = (
    returns_matrix[
        top_funds
    ]
    .dropna()
)

weights = np.array(
    [1 / len(top_funds)] * len(top_funds)
)

portfolio_metrics = calculate_portfolio_metrics(
    returns_matrix,
    weights
)

diversification_score = (
    calculate_diversification_score(
        returns_matrix
    )
)

assert (
    0 <= diversification_score <= 100
)

print(
    f"✓ Portfolio Engine passed"
)

print(
    f"  Diversification Score: "
    f"{diversification_score:.2f}/100"
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 60)
print("ALL FUNDLENS V2 TESTS PASSED")
print("=" * 60)

print("\nFund tested:")
print(fund_name)

print("\nPortfolio funds:")
for fund in top_funds:
    print(f"  - {fund}")

print("\nV2 validation completed successfully.")