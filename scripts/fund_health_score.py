"""
Fund Health Score Engine
FundLens V2 - Mutual Fund Risk & Portfolio Intelligence

Converts risk and performance metrics into an easy-to-understand
0-100 Fund Health Score.
"""

import pandas as pd


def normalize_score(value, minimum, maximum):
    """
    Convert a value into a 0-100 score.
    """
    if pd.isna(value):
        return 50.0

    if maximum == minimum:
        return 50.0

    score = (value - minimum) / (maximum - minimum) * 100

    return max(0.0, min(100.0, score))


def calculate_fund_health_score(metrics):
    """
    Calculate an overall Fund Health Score from 0-100.

    Higher return, Sharpe and Sortino improve the score.
    Lower volatility, drawdown and tail risk improve the score.
    """

    annualized_return = metrics.get("annualized_return")
    volatility = metrics.get("volatility")
    sharpe_ratio = metrics.get("sharpe_ratio")
    sortino_ratio = metrics.get("sortino_ratio")
    max_drawdown = metrics.get("max_drawdown")
    var_95 = metrics.get("var_95")
    cvar_95 = metrics.get("cvar_95")

    # Individual component scores
    return_score = normalize_score(
        annualized_return,
        0.0,
        0.25
    )

    volatility_score = 100 - normalize_score(
        volatility,
        0.05,
        0.30
    )

    sharpe_score = normalize_score(
        sharpe_ratio,
        0.0,
        2.0
    )

    sortino_score = normalize_score(
        sortino_ratio,
        0.0,
        3.0
    )

    # max_drawdown is negative, so less negative = better
    drawdown_score = 100 - normalize_score(
        abs(max_drawdown),
        0.0,
        0.40
    )

    var_score = 100 - normalize_score(
        var_95,
        0.0,
        0.05
    )

    cvar_score = 100 - normalize_score(
        cvar_95,
        0.0,
        0.08
    )

    # Weighted overall score
    weights = {
        "return": 0.20,
        "volatility": 0.15,
        "sharpe": 0.20,
        "sortino": 0.15,
        "drawdown": 0.15,
        "var": 0.075,
        "cvar": 0.075,
    }

    health_score = (
        return_score * weights["return"]
        + volatility_score * weights["volatility"]
        + sharpe_score * weights["sharpe"]
        + sortino_score * weights["sortino"]
        + drawdown_score * weights["drawdown"]
        + var_score * weights["var"]
        + cvar_score * weights["cvar"]
    )

    return round(health_score, 2)


def classify_health_score(score):
    """
    Convert numerical score into a simple category.
    """

    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 50:
        return "Moderate"
    elif score >= 35:
        return "Weak"
    else:
        return "Poor"