"""
FundLens V2 - Fund Health Score Generator

Loads mutual fund NAV data from the SQLite database,
calculates risk metrics and Fund Health Scores for
all available funds, and saves the results to CSV.
"""

import sqlite3
from pathlib import Path

import pandas as pd

from scripts.risk_engine import calculate_risk_metrics
from scripts.fund_health_score import (
    calculate_fund_health_score,
    classify_health_score,
)


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

DB_PATH = Path("data/db/bluestock_mf.db")
OUTPUT_PATH = Path("reports/fund_health_scores.csv")


# ---------------------------------------------------------
# Load NAV data
# ---------------------------------------------------------

def load_nav_data():
    """Load fund NAV history from the SQLite database."""

    connection = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            f.scheme_name,
            n.nav_date,
            n.nav
        FROM fact_nav n
        JOIN dim_fund f
            ON n.amfi_code = f.amfi_code
        ORDER BY
            f.scheme_name,
            n.nav_date
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    return df


# ---------------------------------------------------------
# Calculate metrics for all funds
# ---------------------------------------------------------

def generate_health_scores(nav_data):
    """Calculate risk metrics and health scores for every fund."""

    results = []

    for fund_name, group in nav_data.groupby("scheme_name"):

        nav_series = group["nav"]

        # Calculate risk metrics
        metrics = calculate_risk_metrics(nav_series)

        # Calculate overall health score
        health_score = calculate_fund_health_score(metrics)

        # Convert score into category
        category = classify_health_score(health_score)

        results.append(
            {
                "Fund": fund_name,
                "Annualized Return": metrics["annualized_return"],
                "Volatility": metrics["volatility"],
                "Sharpe Ratio": metrics["sharpe_ratio"],
                "Sortino Ratio": metrics["sortino_ratio"],
                "Maximum Drawdown": metrics["max_drawdown"],
                "VaR 95%": metrics["var_95"],
                "CVaR 95%": metrics["cvar_95"],
                "Health Score": health_score,
                "Category": category,
            }
        )

    return pd.DataFrame(results)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

def save_results(result):
    """Save health scores to the reports directory."""

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
    )


# ---------------------------------------------------------
# Main execution
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("FundLens V2 - Fund Health Score Generator")
    print("=" * 60)

    print("\nLoading NAV data...")

    nav_data = load_nav_data()

    print(f"Loaded {len(nav_data):,} NAV records.")
    print(
        f"Found {nav_data['scheme_name'].nunique()} funds."
    )

    print("\nCalculating risk metrics and health scores...")

    result = generate_health_scores(nav_data)

    # Highest score first
    result = result.sort_values(
        "Health Score",
        ascending=False,
    ).reset_index(drop=True)

    print("\nHealth score calculation completed.")

    print("\nTop 5 funds by Health Score:")
    print(
        result[
            [
                "Fund",
                "Health Score",
                "Category",
            ]
        ].head(5).to_string(index=False)
    )

    print("\nHealth category distribution:")
    print(
        result["Category"]
        .value_counts()
        .to_string()
    )

    save_results(result)

    print(
        f"\nResults saved to: {OUTPUT_PATH}"
    )

    print("\n" + "=" * 60)
    print("Fund Health Score generation completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()