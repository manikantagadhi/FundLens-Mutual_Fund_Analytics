# FundLens V2 — Mutual Fund Risk & Portfolio Intelligence Platform

FundLens V2 is an enhanced mutual fund analytics platform designed to analyze
mutual fund performance, risk, portfolio behavior, and simulated future
outcomes using historical NAV data.

The project builds upon an existing open-source mutual fund analytics
implementation and extends it with additional risk analytics, fund health
scoring, peer comparison, Monte Carlo simulation, portfolio analysis, and an
interactive Streamlit dashboard.

---

## 📌 Project Overview

Mutual fund investors need more than historical returns to understand the
behavior of a fund. Returns should be considered together with volatility,
drawdown, risk-adjusted performance, downside risk, diversification, and
portfolio-level behavior.

FundLens V2 provides an interactive platform for exploring these aspects
using historical mutual fund NAV data.

The platform combines:

- Mutual fund performance analysis
- Risk measurement
- Risk-adjusted performance metrics
- Fund health scoring
- Peer comparison
- Monte Carlo simulation
- Portfolio analytics
- Correlation analysis
- Diversification analysis
- Interactive visualization

---

# 🎯 Problem Statement

Traditional mutual fund analysis often focuses heavily on returns.

However, a fund with high returns may also have:

- High volatility
- Large drawdowns
- Poor downside-risk characteristics
- Weak risk-adjusted performance
- High correlation with other funds

Therefore, investors and analysts need a system that evaluates mutual funds
from multiple dimensions instead of relying only on historical returns.

FundLens V2 addresses this requirement by combining performance, risk,
comparative, simulation, and portfolio-level analytics in a single platform.

---

# 🚀 V2 Objectives

The major objectives of FundLens V2 are:

1. Analyze historical mutual fund performance using NAV data.
2. Calculate important risk and risk-adjusted performance metrics.
3. Generate a composite Fund Health Score.
4. Compare funds with their peer universe.
5. Simulate possible future investment outcomes using Monte Carlo simulation.
6. Analyze portfolios containing multiple mutual funds.
7. Measure portfolio diversification and fund correlations.
8. Provide an interactive dashboard for analysis and visualization.
9. Validate the analytical modules through automated tests.
10. Provide a reusable analytical architecture for future enhancements.

---

# ⭐ Key V2 Features

## 1. Risk Engine

The Risk Engine calculates multiple performance and risk metrics from
historical NAV data.

### Metrics

- Annualized Return
- Annualized Volatility
- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- Historical Value at Risk (VaR)
- Conditional Value at Risk (CVaR)

The engine is implemented as a reusable Python module so that the same
calculations can be used by the dashboard and validation scripts.

---

## 2. Fund Health Score

FundLens V2 introduces a composite Fund Health Score ranging from 0 to 100.

The score combines multiple dimensions of fund behavior:

| Metric | Weight |
|---|---:|
| Annualized Return | 20% |
| Volatility | 15% |
| Sharpe Ratio | 20% |
| Sortino Ratio | 15% |
| Maximum Drawdown | 15% |
| VaR | 7.5% |
| CVaR | 7.5% |

### Health Categories

| Score | Category |
|---:|---|
| 80–100 | Excellent |
| 65–79 | Good |
| 50–64 | Moderate |
| 35–49 | Weak |
| 0–34 | Poor |

> The Fund Health Score is a project-defined analytical score and is not an
> official rating or investment recommendation.

---

## 3. Peer Comparison

FundLens V2 provides comparative analysis of a selected fund against the
available fund universe.

The comparison includes percentile-based measurements such as:

- Health Score percentile
- Return percentile
- Sharpe Ratio percentile
- Volatility percentile
- Drawdown percentile

This helps identify how a selected fund behaves relative to other funds in
the dataset.

---

## 4. Monte Carlo Simulation

The Monte Carlo module uses historical daily return behavior to simulate
multiple possible future investment paths.

Users can configure:

- Initial investment
- Investment period
- Number of simulations

The dashboard presents:

- Median simulated value
- 10th percentile
- 25th percentile
- 75th percentile
- 90th percentile
- Minimum simulated value
- Maximum simulated value
- Simulation distribution

The simulation is intended for analytical scenario exploration rather than
prediction or guaranteed future-return estimation.

---

## 5. Portfolio Intelligence

FundLens V2 allows users to construct a portfolio using multiple mutual
funds.

Users can:

- Select multiple funds
- Assign portfolio weights
- Validate total allocation
- Calculate portfolio returns
- Calculate portfolio volatility
- Calculate Sharpe Ratio
- Calculate Sortino Ratio
- Calculate Maximum Drawdown
- Calculate diversification score
- Examine fund correlations
- Analyze return contribution

### Portfolio Metrics

The Portfolio Engine combines individual fund return series and portfolio
weights to calculate portfolio-level analytics.

---

## 6. Diversification Analysis

The portfolio module analyzes the correlation between selected funds.

A diversification score is calculated from the average pairwise correlation
between the selected funds.

Lower average correlation indicates greater diversification potential.

The resulting score is normalized to a 0–100 scale.

---

# 📊 Interactive Dashboard

FundLens V2 uses Streamlit to provide an interactive web dashboard.

The dashboard contains five major sections:

### 📈 Fund Performance

Provides historical NAV and performance visualization.

### 🛡️ Risk & Fund Health

Displays:

- Fund Health Score
- Health category
- Annualized return
- Volatility
- Sharpe Ratio
- Sortino Ratio
- Maximum Drawdown
- VaR
- CVaR
- Peer comparison

### 📊 Macro Industry Trends

Provides analysis of broader dataset-level trends such as:

- SIP inflows
- AUM
- Fund-level trends

### 🎲 Monte Carlo Simulation

Allows users to configure investment assumptions and visualize simulated
future outcomes.

### 💼 Portfolio Intelligence

Allows users to construct and analyze a multi-fund portfolio.

---

# 🏗️ System Architecture

```text
                  ┌───────────────────────┐
                  │   Mutual Fund Data    │
                  │      / SQLite DB      │
                  └───────────┬───────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │      Data Engine      │
                  │ NAV / SIP / AUM Data  │
                  └───────────┬───────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
      ┌─────────────┐  ┌──────────────┐  ┌───────────────┐
      │ Risk Engine │  │ Health Score │  │ Peer Compare  │
      └──────┬──────┘  └──────┬───────┘  └───────┬───────┘
             │                │                  │
             └────────────────┼──────────────────┘
                              │
             ┌────────────────┴────────────────┐
             │                                 │
             ▼                                 ▼
      ┌───────────────┐                 ┌────────────────┐
      │ Monte Carlo   │                 │ Portfolio      │
      │ Simulation    │                 │ Intelligence   │
      └───────┬───────┘                 └───────┬────────┘
              │                                 │
              └────────────────┬────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Dashboard │
                    └─────────────────────┘