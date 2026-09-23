import numpy as np
import pandas as pd


TRADING_DAYS = 252


def calculate_daily_returns(nav_series):
    """
    Calculate daily percentage returns from NAV values.
    """
    nav_series = pd.Series(nav_series).dropna()

    if len(nav_series) < 2:
        raise ValueError("At least two NAV observations are required.")

    returns = nav_series.pct_change().dropna()

    return returns


def run_monte_carlo(
    nav_series,
    initial_investment=100000,
    years=5,
    simulations=1000,
    random_seed=42
):
    """
    Run Monte Carlo simulation using historical daily returns.

    Parameters
    ----------
    nav_series : pandas Series
        Historical NAV values.

    initial_investment : float
        Starting investment amount.

    years : int
        Number of years to simulate.

    simulations : int
        Number of simulation paths.

    random_seed : int
        Seed for reproducible results.

    Returns
    -------
    dict
        Simulation results and summary statistics.
    """

    if initial_investment <= 0:
        raise ValueError("Initial investment must be greater than zero.")

    if years <= 0:
        raise ValueError("Investment period must be greater than zero.")

    if simulations <= 0:
        raise ValueError("Number of simulations must be greater than zero.")

    returns = calculate_daily_returns(nav_series)

    if len(returns) < 30:
        raise ValueError("Not enough historical return data for simulation.")

    mean_daily_return = returns.mean()
    daily_volatility = returns.std()

    total_days = years * TRADING_DAYS

    rng = np.random.default_rng(random_seed)

    random_returns = rng.normal(
        loc=mean_daily_return,
        scale=daily_volatility,
        size=(simulations, total_days)
    )

    growth_paths = np.cumprod(1 + random_returns, axis=1)

    portfolio_paths = initial_investment * growth_paths

    final_values = portfolio_paths[:, -1]

    summary = {
        "initial_investment": initial_investment,
        "years": years,
        "simulations": simulations,
        "mean_daily_return": mean_daily_return,
        "daily_volatility": daily_volatility,
        "median_final_value": np.percentile(final_values, 50),
        "percentile_10": np.percentile(final_values, 10),
        "percentile_25": np.percentile(final_values, 25),
        "percentile_75": np.percentile(final_values, 75),
        "percentile_90": np.percentile(final_values, 90),
        "mean_final_value": np.mean(final_values),
        "minimum_final_value": np.min(final_values),
        "maximum_final_value": np.max(final_values),
    }

    return {
        "paths": portfolio_paths,
        "final_values": final_values,
        "summary": summary,
    }


def create_simulation_dataframe(result):
    """
    Convert simulation paths into a DataFrame.

    Each row represents a simulation.
    Each column represents a trading day.
    """

    paths = result["paths"]

    return pd.DataFrame(paths)


def create_percentile_dataframe(result):
    """
    Create percentile bands across simulation paths.
    """

    paths = result["paths"]

    percentile_data = {
        "day": np.arange(1, paths.shape[1] + 1),
        "p10": np.percentile(paths, 10, axis=0),
        "p25": np.percentile(paths, 25, axis=0),
        "p50": np.percentile(paths, 50, axis=0),
        "p75": np.percentile(paths, 75, axis=0),
        "p90": np.percentile(paths, 90, axis=0),
    }

    return pd.DataFrame(percentile_data)