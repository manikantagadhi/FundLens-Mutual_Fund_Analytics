import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_returns_matrix(nav_data):
    """
    Convert NAV data into a daily return matrix.

    Parameters
    ----------
    nav_data : pandas.DataFrame
        Must contain:
        scheme_name
        nav_date
        nav

    Returns
    -------
    pandas.DataFrame
        Daily returns for each selected fund.
    """

    required_columns = {
        "scheme_name",
        "nav_date",
        "nav"
    }

    missing = required_columns - set(nav_data.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    prices = nav_data.pivot_table(
        index="nav_date",
        columns="scheme_name",
        values="nav"
    )

    prices = prices.sort_index()

    returns = prices.pct_change()

    returns = returns.dropna(
        how="all"
    )

    return returns


def calculate_portfolio_metrics(
    returns,
    weights,
    risk_free_rate=0.065
):
    """
    Calculate portfolio-level risk and performance metrics.
    """

    if returns.empty:
        raise ValueError(
            "Return data is empty."
        )

    weights = np.array(
        weights,
        dtype=float
    )

    if len(weights) != len(returns.columns):
        raise ValueError(
            "Number of weights must match number of funds."
        )

    if np.any(weights < 0):
        raise ValueError(
            "Portfolio weights cannot be negative."
        )

    if not np.isclose(
        weights.sum(),
        1.0
    ):
        raise ValueError(
            "Portfolio weights must sum to 1."
        )

    # Portfolio daily returns
    portfolio_returns = returns.dot(
        weights
    )

    # Annualized return
    cumulative_return = (
        1 + portfolio_returns
    ).prod()

    years = len(
        portfolio_returns
    ) / TRADING_DAYS

    annualized_return = (
        cumulative_return
        ** (1 / years)
    ) - 1

    # Annualized volatility
    annualized_volatility = (
        portfolio_returns.std()
        * np.sqrt(TRADING_DAYS)
    )

    # Sharpe ratio
    if annualized_volatility > 0:
        sharpe_ratio = (
            annualized_return
            - risk_free_rate
        ) / annualized_volatility
    else:
        sharpe_ratio = 0

    # Maximum drawdown
    wealth_index = (
        1 + portfolio_returns
    ).cumprod()

    running_max = wealth_index.cummax()

    drawdown = (
        wealth_index / running_max
    ) - 1

    max_drawdown = drawdown.min()

    # Downside deviation
    downside_returns = portfolio_returns[
        portfolio_returns < 0
    ]

    if len(downside_returns) > 0:
        downside_deviation = (
            downside_returns.std()
            * np.sqrt(TRADING_DAYS)
        )
    else:
        downside_deviation = 0

    if downside_deviation > 0:
        sortino_ratio = (
            annualized_return
            - risk_free_rate
        ) / downside_deviation
    else:
        sortino_ratio = 0

    return {
        "annualized_return":
            annualized_return,

        "annualized_volatility":
            annualized_volatility,

        "sharpe_ratio":
            sharpe_ratio,

        "sortino_ratio":
            sortino_ratio,

        "max_drawdown":
            max_drawdown
    }


def calculate_diversification_score(
    returns
):
    """
    Calculate a simple diversification score
    based on average pairwise correlation.

    Lower correlation indicates greater
    diversification potential.
    """

    if returns.shape[1] < 2:
        return 0.0

    correlation_matrix = returns.corr()

    correlations = correlation_matrix.values

    upper_triangle = correlations[
        np.triu_indices_from(
            correlations,
            k=1
        )
    ]

    if len(upper_triangle) == 0:
        return 0.0

    average_correlation = np.nanmean(
        upper_triangle
    )

    diversification_score = (
        1 - average_correlation
    ) * 100

    diversification_score = np.clip(
        diversification_score,
        0,
        100
    )

    return diversification_score


def build_portfolio_summary(
    funds,
    weights,
    metrics,
    diversification_score
):
    """
    Create a readable portfolio summary.
    """

    summary = pd.DataFrame({
        "Fund": funds,
        "Weight": [
            weight * 100
            for weight in weights
        ]
    })

    summary["Weight"] = summary[
        "Weight"
    ].round(2)

    return summary