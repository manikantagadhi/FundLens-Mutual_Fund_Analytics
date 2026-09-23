"""
FundLens V2 - Fund Comparison Engine

Compares a selected mutual fund against the complete
FundLens fund universe using risk and health metrics.
"""

import pandas as pd


def calculate_percentile(value, series):
    """
    Calculate the percentile position of a fund
    within the available fund universe.
    """

    series = pd.Series(series).dropna()

    if len(series) == 0:
        return 50.0

    percentile = (
        (series < value).sum() / len(series)
    ) * 100

    return round(percentile, 2)


def compare_fund(selected_fund, health_data):
    """
    Compare the selected fund against all available funds.
    """

    selected = health_data[
        health_data["Fund"] == selected_fund
    ]

    if selected.empty:
        raise ValueError(
            f"Fund not found: {selected_fund}"
        )

    fund = selected.iloc[0]

    comparison = {
        "Health Score Percentile": calculate_percentile(
            fund["Health Score"],
            health_data["Health Score"]
        ),

        "Return Percentile": calculate_percentile(
            fund["Annualized Return"],
            health_data["Annualized Return"]
        ),

        "Sharpe Percentile": calculate_percentile(
            fund["Sharpe Ratio"],
            health_data["Sharpe Ratio"]
        ),

        "Volatility Percentile": calculate_percentile(
            fund["Volatility"],
            health_data["Volatility"]
        ),

        "Drawdown Percentile": calculate_percentile(
            abs(fund["Maximum Drawdown"]),
            abs(health_data["Maximum Drawdown"])
        ),
    }

    return comparison


def generate_peer_summary(selected_fund, health_data):
    """
    Generate a compact comparison summary for the
    selected fund.
    """

    selected = health_data[
        health_data["Fund"] == selected_fund
    ]

    if selected.empty:
        return pd.DataFrame()

    score = selected.iloc[0]["Health Score"]

    peer_data = health_data.copy()

    peer_data["Score Difference"] = (
        peer_data["Health Score"] - score
    )

    peer_data = peer_data[
        peer_data["Fund"] != selected_fund
    ]

    peer_data = peer_data.sort_values(
        "Score Difference",
        ascending=False
    )

    return peer_data[
        [
            "Fund",
            "Health Score",
            "Category",
            "Annualized Return",
            "Volatility",
            "Sharpe Ratio",
            "Maximum Drawdown",
        ]
    ].head(5)