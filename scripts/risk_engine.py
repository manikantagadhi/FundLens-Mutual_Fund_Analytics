import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_daily_returns(nav_series):
    """
    Calculate daily percentage returns from a NAV series.

    Uses a fast path when the input is already numeric,
    while preserving the original behavior for non-numeric data.
    """

    if pd.api.types.is_numeric_dtype(nav_series):
        nav_series = nav_series.dropna()
    else:
        nav_series = pd.to_numeric(
            nav_series,
            errors="coerce"
        ).dropna()

    if len(nav_series) < 2:
        return pd.Series(dtype=float)

    return nav_series.pct_change().dropna()


def calculate_annualized_return(daily_returns):
    """
    Estimate annualized return from average daily return.
    """
    if daily_returns.empty:
        return np.nan

    return daily_returns.mean() * TRADING_DAYS


def calculate_volatility(daily_returns):
    """
    Calculate annualized volatility.
    """
    if daily_returns.empty:
        return np.nan

    return daily_returns.std() * np.sqrt(TRADING_DAYS)


def calculate_sharpe_ratio(daily_returns, risk_free_rate=0.065):
    """
    Calculate the annualized Sharpe Ratio.
    """
    annual_return = calculate_annualized_return(daily_returns)
    volatility = calculate_volatility(daily_returns)

    if pd.isna(volatility) or volatility == 0:
        return np.nan

    return (annual_return - risk_free_rate) / volatility


def calculate_sortino_ratio(daily_returns, risk_free_rate=0.065):
    """
    Calculate the annualized Sortino Ratio using downside volatility.
    """
    annual_return = calculate_annualized_return(daily_returns)

    downside_returns = daily_returns[daily_returns < 0]

    if len(downside_returns) < 2:
        return np.nan

    downside_volatility = (
        downside_returns.std() * np.sqrt(TRADING_DAYS)
    )

    if downside_volatility == 0:
        return np.nan

    return (annual_return - risk_free_rate) / downside_volatility


def calculate_max_drawdown(nav_series):
    """
    Calculate maximum drawdown from a NAV series.
    """
    nav_series = pd.to_numeric(nav_series, errors="coerce").dropna()

    if nav_series.empty:
        return np.nan

    running_max = nav_series.cummax()
    drawdown = (nav_series / running_max) - 1

    return drawdown.min()


def calculate_historical_var(daily_returns, confidence_level=0.95):
    """
    Calculate historical Value at Risk (VaR).

    Returns a positive percentage representing the potential
    loss threshold.
    """
    if daily_returns.empty:
        return np.nan

    percentile = (1 - confidence_level) * 100

    return -np.percentile(daily_returns, percentile)


def calculate_cvar(daily_returns, confidence_level=0.95):
    """
    Calculate Conditional Value at Risk (CVaR).

    Measures the average loss beyond the VaR threshold.
    """
    if daily_returns.empty:
        return np.nan

    var = calculate_historical_var(
        daily_returns,
        confidence_level
    )

    loss_threshold = -var

    tail_losses = daily_returns[daily_returns <= loss_threshold]

    if tail_losses.empty:
        return np.nan

    return -tail_losses.mean()


def calculate_risk_metrics(nav_series, risk_free_rate=0.065):
    """
    Calculate all major risk and performance metrics
    for a single mutual fund.
    """
    daily_returns = calculate_daily_returns(nav_series)

    return {
        "annualized_return": calculate_annualized_return(daily_returns),
        "volatility": calculate_volatility(daily_returns),
        "sharpe_ratio": calculate_sharpe_ratio(
            daily_returns,
            risk_free_rate
        ),
        "sortino_ratio": calculate_sortino_ratio(
            daily_returns,
            risk_free_rate
        ),
        "max_drawdown": calculate_max_drawdown(nav_series),
        "var_95": calculate_historical_var(
            daily_returns,
            confidence_level=0.95
        ),
        "cvar_95": calculate_cvar(
            daily_returns,
            confidence_level=0.95
        ),
    }