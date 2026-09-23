import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os
import numpy as np

from scripts.fund_comparison import compare_fund, generate_peer_summary
from scripts.monte_carlo import run_monte_carlo, create_percentile_dataframe
from scripts.portfolio_engine import (
    calculate_returns_matrix,
    calculate_portfolio_metrics,
    calculate_diversification_score,
    build_portfolio_summary
)

# ==========================================
# 1. PAGE CONFIG & PREMIUM CSS
# ==========================================

st.set_page_config(
    page_title="FundLens V2 - Mutual Fund Analytics",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b101a;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stSidebar"] {
        background-color: #121826;
        border-right: 1px solid #1e293b;
    }

    [data-testid="stMetricValue"] {
        color: #38bdf8;
        font-size: 2rem;
        font-weight: 700;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        border-bottom: 1px solid #1e293b;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        color: #94a3b8;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0 20px;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        color: #ffffff;
        border-bottom: 3px solid #38bdf8;
        background-color: rgba(56, 189, 248, 0.1);
        border-radius: 5px 5px 0 0;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 2. HEADER SECTION
# ==========================================

col_logo, col_title = st.columns([1, 15])

with col_logo:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2933/2933116.png",
        width=60
    )

with col_title:
    st.markdown(
        """
        <h1 style='margin-bottom: 0px; padding-bottom: 0px; line-height: 1.2;'>
        FundLens V2
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='color: #94a3b8; font-size: 1.1rem;'>
        Mutual Fund Performance, Risk & Portfolio Intelligence Platform
        </p>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    "<hr style='border: 1px solid #1e293b; margin-top: 5px;'>",
    unsafe_allow_html=True
)


# ==========================================
# 3. DATA ENGINE
# ==========================================

@st.cache_data
def get_data():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(
        base_dir,
        "data",
        "db",
        "bluestock_mf.db"
    )

    conn = sqlite3.connect(db_path)

    # -------------------------------
    # NAV DATA
    # -------------------------------

    query_nav = """
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

    try:
        df_nav = pd.read_sql_query(query_nav, conn)

    except Exception:

        df_nav = pd.read_sql_query(
            "SELECT * FROM fact_nav",
            conn
        )

        df_nav["scheme_name"] = (
            df_nav["amfi_code"].astype(str)
        )

    # -------------------------------
    # SIP DATA
    # -------------------------------

    try:

        df_sip = pd.read_sql_query(
            "SELECT * FROM fact_sip_industry",
            conn
        )

    except Exception:

        sip_path = os.path.join(
            base_dir,
            "data",
            "raw",
            "04_monthly_sip_inflows.csv"
        )

        if os.path.exists(sip_path):
            df_sip = pd.read_csv(sip_path)
        else:
            df_sip = pd.DataFrame()

    # -------------------------------
    # AUM DATA
    # -------------------------------

    try:

        df_aum = pd.read_sql_query(
            "SELECT * FROM fact_aum",
            conn
        )

    except Exception:

        aum_path = os.path.join(
            base_dir,
            "data",
            "raw",
            "03_aum_by_fund_house.csv"
        )

        if os.path.exists(aum_path):
            df_aum = pd.read_csv(aum_path)
        else:
            df_aum = pd.DataFrame()

    conn.close()

    df_nav["nav_date"] = pd.to_datetime(
        df_nav["nav_date"]
    )

    return df_nav, df_sip, df_aum


df_nav, df_sip, df_aum = get_data()


# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================

st.sidebar.markdown(
    "<h3 style='color: #ffffff;'>Filter Parameters</h3>",
    unsafe_allow_html=True
)

scheme_list = df_nav["scheme_name"].unique()

selected_scheme = st.sidebar.selectbox(
    "Select Asset / Mutual Fund Scheme",
    scheme_list
)

min_date = df_nav["nav_date"].min().date()
max_date = df_nav["nav_date"].max().date()

st.sidebar.markdown(
    "<hr style='border: 1px solid #1e293b;'>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    "<h4 style='color: #94a3b8;'>Date Range</h4>",
    unsafe_allow_html=True
)

try:

    start_date, end_date = st.sidebar.date_input(
        "Select Trading Period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

except ValueError:

    st.sidebar.error(
        "Please select both start and end dates."
    )

    start_date, end_date = min_date, max_date


filtered_data = df_nav[
    (df_nav["scheme_name"] == selected_scheme)
    &
    (df_nav["nav_date"].dt.date >= start_date)
    &
    (df_nav["nav_date"].dt.date <= end_date)
].sort_values(
    by="nav_date"
)


# ==========================================
# 5. LOAD FUND HEALTH DATA
# ==========================================

base_dir = os.path.dirname(
    os.path.abspath(__file__)
)

health_path = os.path.join(
    base_dir,
    "reports",
    "fund_health_scores.csv"
)

if os.path.exists(health_path):

    health_data = pd.read_csv(
        health_path
    )

else:

    health_data = pd.DataFrame()


# ==========================================
# 6. INTERACTIVE TABS
# ==========================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Fund Performance",
    "🛡️ Risk & Fund Health",
    "📊 Macro Industry Trends",
    "🎲 Monte Carlo Simulation",
    "💼 Portfolio Intelligence"
])


# =========================================================
# TAB 1 — FUND PERFORMANCE
# =========================================================

with tab1:

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    if not filtered_data.empty:

        latest_date = filtered_data[
            "nav_date"
        ].max()

        latest_nav = filtered_data[
            filtered_data["nav_date"] == latest_date
        ]["nav"].values[0]

        total_records = len(
            filtered_data
        )

        with col1:

            st.metric(
                label="Latest Net Asset Value (NAV)",
                value=f"₹ {latest_nav:.2f}"
            )

        with col2:

            st.metric(
                label="Last Updated",
                value=str(latest_date.date())
            )

        with col3:

            st.metric(
                label="Trading Days Captured",
                value=total_records
            )

        st.markdown(
            "<hr style='border: 1px solid #1e293b; margin: 20px 0;'>",
            unsafe_allow_html=True
        )

        chart_col, table_col = st.columns(
            [2.8, 1.2]
        )

        # -------------------------------
        # NAV CHART
        # -------------------------------

        with chart_col:

            st.markdown(
                """
                <h4 style='color: #e2e8f0;'>
                Historical NAV Trajectory
                </h4>
                """,
                unsafe_allow_html=True
            )

            fig_nav = px.area(
                filtered_data,
                x="nav_date",
                y="nav",
                title=""
            )

            fig_nav.update_traces(
                line_color="#38bdf8",
                fillcolor="rgba(56, 189, 248, 0.1)"
            )

            fig_nav.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    showgrid=False,
                    title=""
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#1e293b",
                    title="NAV (₹)"
                ),
                margin=dict(
                    l=0,
                    r=0,
                    t=10,
                    b=0
                )
            )

            st.plotly_chart(
                fig_nav,
                width="stretch"
            )

        # -------------------------------
        # RECENT DATA
        # -------------------------------

        with table_col:

            st.markdown(
                """
                <h4 style='color: #e2e8f0;'>
                Recent Data Log
                </h4>
                """,
                unsafe_allow_html=True
            )

            recent_data = (
                filtered_data[
                    ["nav_date", "nav"]
                ]
                .sort_values(
                    by="nav_date",
                    ascending=False
                )
                .head(15)
            )

            recent_data["nav_date"] = (
                recent_data["nav_date"]
                .dt.strftime("%Y-%m-%d")
            )

            st.dataframe(
                recent_data,
                width="stretch",
                hide_index=True
            )

            st.markdown(
                "<br>",
                unsafe_allow_html=True
            )

            csv = (
                filtered_data
                .to_csv(index=False)
                .encode("utf-8")
            )

            st.download_button(
                label="Download Data (CSV)",
                data=csv,
                file_name=f"{selected_scheme}_data.csv",
                mime="text/csv",
                width="stretch"
            )

    else:

        st.warning(
            "No data available for the selected date range. "
            "Please adjust the calendar filter."
        )


# =========================================================
# TAB 2 — RISK & FUND HEALTH
# =========================================================

with tab2:

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h2 style='color: #ffffff;'>
        🛡️ Risk & Fund Health
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='color: #94a3b8;'>
        Risk-adjusted analysis and overall health assessment
        for the selected mutual fund.
        </p>
        """,
        unsafe_allow_html=True
    )

    if not health_data.empty:

        selected_health = health_data[
            health_data["Fund"] == selected_scheme
        ]

        if not selected_health.empty:

            fund_health = selected_health.iloc[0]

            # -----------------------------------------
            # FUND HEALTH OVERVIEW
            # -----------------------------------------

            st.markdown(
                """
                <h3 style='color: #ffffff;'>
                Fund Health Overview
                </h3>
                """,
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Health Score",
                    f"{fund_health['Health Score']:.2f} / 100"
                )

            with col2:

                st.metric(
                    "Health Category",
                    fund_health["Category"]
                )

            with col3:

                st.metric(
                    "Annualized Return",
                    f"{fund_health['Annualized Return'] * 100:.2f}%"
                )

            st.markdown(
                "<hr style='border: 1px solid #1e293b; margin: 20px 0;'>",
                unsafe_allow_html=True
            )

            # -----------------------------------------
            # RISK METRICS
            # -----------------------------------------

            st.markdown(
                """
                <h3 style='color: #ffffff;'>
                📊 Risk Metrics
                </h3>
                """,
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Volatility",
                    f"{fund_health['Volatility'] * 100:.2f}%"
                )

            with col2:

                st.metric(
                    "Sharpe Ratio",
                    f"{fund_health['Sharpe Ratio']:.2f}"
                )

            with col3:

                st.metric(
                    "Sortino Ratio",
                    f"{fund_health['Sortino Ratio']:.2f}"
                )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Maximum Drawdown",
                    f"{fund_health['Maximum Drawdown'] * 100:.2f}%"
                )

            with col2:

                st.metric(
                    "VaR 95%",
                    f"{fund_health['VaR 95%'] * 100:.2f}%"
                )

            with col3:

                st.metric(
                    "CVaR 95%",
                    f"{fund_health['CVaR 95%'] * 100:.2f}%"
                )

            st.markdown(
                "<hr style='border: 1px solid #1e293b; margin: 20px 0;'>",
                unsafe_allow_html=True
            )

            # -----------------------------------------
            # HEALTH SCORE INTERPRETATION
            # -----------------------------------------

            st.markdown(
                """
                <h3 style='color: #ffffff;'>
                💡 Health Score Summary
                </h3>
                """,
                unsafe_allow_html=True
            )

            st.info(
                f"""
                **{selected_scheme}**

                Fund Health Score: **{fund_health['Health Score']:.2f}/100**

                Health Category: **{fund_health['Category']}**

                The score combines return and risk measures
                including volatility, Sharpe ratio, Sortino ratio,
                maximum drawdown, VaR and CVaR.
                """
            )


            # -----------------------------------------
            # PEER COMPARISON
            # -----------------------------------------

            st.markdown(
                "<hr style='border: 1px solid #1e293b; margin: 25px 0;'>",
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <h3 style='color: #ffffff;'>
                🔎 Peer Comparison
                </h3>
                """,
                unsafe_allow_html=True
            )

            comparison = compare_fund(selected_scheme, health_data)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Health Score Percentile",
                    f"{comparison['Health Score Percentile']:.0f}th"
                )

            with col2:
                st.metric(
                    "Return Percentile",
                    f"{comparison['Return Percentile']:.0f}th"
                )

            with col3:
                st.metric(
                    "Sharpe Percentile",
                    f"{comparison['Sharpe Percentile']:.0f}th"
                )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Volatility Percentile",
                    f"{comparison['Volatility Percentile']:.0f}th"
                )

            with col2:
                st.metric(
                    "Drawdown Percentile",
                    f"{comparison['Drawdown Percentile']:.0f}th"
                )

            st.markdown(
                """
                <p style='color: #94a3b8;'>
                Percentiles show the selected fund's position relative
                to the funds currently included in FundLens.
                </p>
                """,
                unsafe_allow_html=True
            )

            peer_summary = generate_peer_summary(
                selected_scheme,
                health_data
            )

            if not peer_summary.empty:

                st.markdown(
                    """
                    <h4 style='color: #e2e8f0;'>
                    Peer Fund Comparison
                    </h4>
                    """,
                    unsafe_allow_html=True
                )

                display_peers = peer_summary.copy()

                display_peers["Annualized Return"] = (
                    display_peers["Annualized Return"] * 100
                ).round(2).astype(str) + "%"

                display_peers["Volatility"] = (
                    display_peers["Volatility"] * 100
                ).round(2).astype(str) + "%"

                display_peers["Maximum Drawdown"] = (
                    display_peers["Maximum Drawdown"] * 100
                ).round(2).astype(str) + "%"

                display_peers["Health Score"] = (
                    display_peers["Health Score"].round(2)
                )

                display_peers["Sharpe Ratio"] = (
                    display_peers["Sharpe Ratio"].round(2)
                )

                st.dataframe(
                    display_peers,
                    width="stretch",
                    hide_index=True
                )

        else:

            st.warning(
                "Health-score information is not available "
                "for the selected fund."
            )

    else:

        st.error(
            "Fund health data was not found. "
            "Run the Fund Health Score generator first."
        )


# =========================================================
# TAB 3 — MACRO INDUSTRY TRENDS
# =========================================================

with tab3:

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    col_sip, col_aum = st.columns(2)

    # -----------------------------------------
    # SIP INFLOWS
    # -----------------------------------------

    with col_sip:

        if not df_sip.empty:

            st.markdown(
                """
                <h4 style='color: #e2e8f0;'>
                Monthly SIP Inflows
                </h4>
                """,
                unsafe_allow_html=True
            )

            x_col = df_sip.columns[0]
            y_col = df_sip.columns[1]

            fig_sip = px.bar(
                df_sip,
                x=x_col,
                y=y_col
            )

            fig_sip.update_traces(
                marker_color="#f59e0b"
            )

            fig_sip.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    showgrid=False,
                    title="Month"
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#1e293b",
                    title="Inflow (Cr)"
                ),
                margin=dict(
                    l=0,
                    r=0,
                    t=10,
                    b=0
                )
            )

            st.plotly_chart(
                fig_sip,
                width="stretch"
            )

        else:

            st.info(
                "SIP Inflow data not available."
            )

    # -----------------------------------------
    # AUM
    # -----------------------------------------

    with col_aum:

        if not df_aum.empty:

            st.markdown(
                """
                <h4 style='color: #e2e8f0;'>
                Top Fund Houses by AUM
                </h4>
                """,
                unsafe_allow_html=True
            )

            x_col = df_aum.columns[0]
            y_col = df_aum.columns[2]

            aum_agg = (
                df_aum
                .groupby(x_col)[y_col]
                .max()
                .reset_index()
                .sort_values(
                    by=y_col,
                    ascending=False
                )
                .head(10)
            )

            fig_aum = px.bar(
                aum_agg,
                x=x_col,
                y=y_col
            )

            fig_aum.update_traces(
                marker_color="#10b981"
            )

            fig_aum.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(
                    showgrid=False,
                    title="Asset Management Company"
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="#1e293b",
                    title="AUM (Cr)"
                ),
                margin=dict(
                    l=0,
                    r=0,
                    t=10,
                    b=0
                )
            )

            st.plotly_chart(
                fig_aum,
                width="stretch"
            )

        else:

            st.info(
                "AUM data not available."
            )

            # ============================================================
# TAB 4 — MONTE CARLO SIMULATION
# ============================================================

with tab4:

    st.subheader("🎲 Monte Carlo Simulation")
    st.write(
        "Simulate possible future investment outcomes using "
        "historical return and volatility characteristics."
    )

    st.warning(
        "⚠️ Monte Carlo results are statistical scenarios, "
        "not guaranteed predictions of future returns."
    )

    # --------------------------------------------------------
    # Simulation Inputs
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        initial_investment = st.number_input(
            "Initial Investment (₹)",
            min_value=1000,
            value=100000,
            step=10000
        )

    with col2:
        investment_years = st.slider(
            "Investment Period (Years)",
            min_value=1,
            max_value=20,
            value=5
        )

    with col3:
        simulations = st.selectbox(
            "Number of Simulations",
            [500, 1000, 2500, 5000],
            index=1
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Run Simulation
    # --------------------------------------------------------

    if st.button(
        "🚀 Run Monte Carlo Simulation",
        type="primary"
    ):

        try:

            selected_nav = df_nav[
                df_nav["scheme_name"] == selected_scheme
            ].sort_values("nav_date")

            if selected_nav.empty:
                st.error(
                    "No NAV data available for the selected fund."
                )

            else:

                result = run_monte_carlo(
                    selected_nav["nav"],
                    initial_investment=initial_investment,
                    years=investment_years,
                    simulations=simulations
                )

                summary = result["summary"]

                # ------------------------------------------------
                # Results
                # ------------------------------------------------

                st.success(
                    f"Simulation completed for "
                    f"**{selected_scheme}**"
                )

                st.markdown("### 📊 Simulation Results")

                metric1, metric2, metric3, metric4 = st.columns(4)

                with metric1:
                    st.metric(
                        "Initial Investment",
                        f"₹{summary['initial_investment']:,.0f}"
                    )

                with metric2:
                    st.metric(
                        "Median Value",
                        f"₹{summary['median_final_value']:,.0f}"
                    )

                with metric3:
                    st.metric(
                        "10th Percentile",
                        f"₹{summary['percentile_10']:,.0f}"
                    )

                with metric4:
                    st.metric(
                        "90th Percentile",
                        f"₹{summary['percentile_90']:,.0f}"
                    )

                # ------------------------------------------------
                # Percentile Table
                # ------------------------------------------------

                st.markdown("### 📋 Future Value Scenarios")

                scenario_data = pd.DataFrame({
                    "Scenario": [
                        "10th Percentile",
                        "25th Percentile",
                        "Median (50th)",
                        "75th Percentile",
                        "90th Percentile"
                    ],
                    "Projected Value": [
                        summary["percentile_10"],
                        summary["percentile_25"],
                        summary["median_final_value"],
                        summary["percentile_75"],
                        summary["percentile_90"]
                    ]
                })

                scenario_data["Projected Value"] = (
                    scenario_data["Projected Value"]
                    .map(lambda x: f"₹{x:,.0f}")
                )

                st.dataframe(
                    scenario_data,
                    width="stretch",
                    hide_index=True
                )

                # ------------------------------------------------
                # Simulation Chart
                # ------------------------------------------------

                st.markdown(
                    "### 📈 Simulated Portfolio Value"
                )

                percentile_df = create_percentile_dataframe(
                    result
                )

                chart_df = percentile_df.copy()

                chart_df["Year"] = (
                    chart_df["day"] / 252
                )

                chart_df = chart_df[
                    chart_df["day"] % 21 == 0
                ]

                chart_df = chart_df.melt(
                    id_vars=["day", "Year"],
                    value_vars=[
                        "p10",
                        "p25",
                        "p50",
                        "p75",
                        "p90"
                    ],
                    var_name="Percentile",
                    value_name="Portfolio Value"
                )

                fig_mc = px.line(
                    chart_df,
                    x="Year",
                    y="Portfolio Value",
                    color="Percentile",
                    title=(
                        "Monte Carlo Future Portfolio "
                        "Value Scenarios"
                    )
                )

                fig_mc.update_layout(
                    xaxis_title="Investment Period (Years)",
                    yaxis_title="Portfolio Value (₹)",
                    hovermode="x unified"
                )

                st.plotly_chart(
                    fig_mc,
                    width="stretch"
                )

                # ------------------------------------------------
                # Simulation Statistics
                # ------------------------------------------------

                st.markdown(
                    "### 📌 Simulation Statistics"
                )

                stat1, stat2, stat3 = st.columns(3)

                with stat1:
                    st.metric(
                        "Average Final Value",
                        f"₹{summary['mean_final_value']:,.0f}"
                    )

                with stat2:
                    st.metric(
                        "Minimum Final Value",
                        f"₹{summary['minimum_final_value']:,.0f}"
                    )

                with stat3:
                    st.metric(
                        "Maximum Final Value",
                        f"₹{summary['maximum_final_value']:,.0f}"
                    )

        except Exception as e:

            st.error(
                f"Unable to run Monte Carlo simulation: {e}"
            )

            # ============================================================
# TAB 5 — PORTFOLIO INTELLIGENCE
# ============================================================

with tab5:

    st.subheader("💼 Portfolio Intelligence")

    st.write(
        "Build a multi-fund mutual fund portfolio and analyze "
        "its historical return, risk and diversification."
    )

    st.info(
        "Portfolio analysis is based on historical NAV data. "
        "It is an analytical scenario tool and does not guarantee "
        "future investment performance."
    )

    # --------------------------------------------------------
    # Fund Selection
    # --------------------------------------------------------

    st.markdown("### 1️⃣ Select Funds")

    available_funds = sorted(
        df_nav["scheme_name"].dropna().unique()
    )

    selected_funds = st.multiselect(
        "Select 2–5 mutual funds",
        available_funds,
        default=(
            [selected_scheme]
            if selected_scheme in available_funds
            else []
        )
    )

    if len(selected_funds) < 2:

        st.warning(
            "Please select at least 2 funds "
            "to create a portfolio."
        )

    elif len(selected_funds) > 5:

        st.warning(
            "Please select a maximum of 5 funds."
        )

    else:

        # ----------------------------------------------------
        # Allocation
        # ----------------------------------------------------

        st.markdown("### 2️⃣ Set Portfolio Allocation")

        default_weight = round(
            100 / len(selected_funds),
            2
        )

        weight_values = []

        allocation_cols = st.columns(
            len(selected_funds)
        )

        for i, fund in enumerate(selected_funds):

            with allocation_cols[i]:

                weight = st.number_input(
                    fund[:25],
                    min_value=0.0,
                    max_value=100.0,
                    value=default_weight,
                    step=5.0,
                    key=f"portfolio_weight_{i}"
                )

                weight_values.append(weight)

        total_weight = sum(
            weight_values
        )

        st.write(
            f"**Total Allocation: "
            f"{total_weight:.2f}%**"
        )

        if not np.isclose(
            total_weight,
            100.0,
            atol=0.01
        ):

            st.warning(
                "Portfolio allocation must total exactly 100%."
            )

        # ----------------------------------------------------
        # Run Portfolio Analysis
        # ----------------------------------------------------

        if st.button(
            "🚀 Analyze Portfolio",
            type="primary"
        ):

            if not np.isclose(
                total_weight,
                100.0,
                atol=0.01
            ):

                st.error(
                    "Please adjust the allocations so "
                    "they total exactly 100%."
                )

            else:

                try:

                    portfolio_data = df_nav[
                        df_nav["scheme_name"].isin(
                            selected_funds
                        )
                    ][
                        [
                            "scheme_name",
                            "nav_date",
                            "nav"
                        ]
                    ].copy()

                    returns_matrix = (
                        calculate_returns_matrix(
                            portfolio_data
                        )
                    )

                    # Keep common observations
                    returns_matrix = (
                        returns_matrix[
                            selected_funds
                        ]
                        .dropna()
                    )

                    if returns_matrix.empty:

                        st.error(
                            "Not enough common historical "
                            "data for the selected funds."
                        )

                    else:

                        weights = np.array(
                            weight_values
                        ) / 100

                        metrics = (
                            calculate_portfolio_metrics(
                                returns_matrix,
                                weights
                            )
                        )

                        diversification_score = (
                            calculate_diversification_score(
                                returns_matrix
                            )
                        )

                        # ------------------------------------
                        # Results
                        # ------------------------------------

                        st.success(
                            "Portfolio analysis completed successfully."
                        )

                        st.markdown(
                            "### 📊 Portfolio Metrics"
                        )

                        col1, col2, col3, col4 = (
                            st.columns(4)
                        )

                        with col1:

                            st.metric(
                                "Annualized Return",
                                f"{metrics['annualized_return'] * 100:.2f}%"
                            )

                        with col2:

                            st.metric(
                                "Volatility",
                                f"{metrics['annualized_volatility'] * 100:.2f}%"
                            )

                        with col3:

                            st.metric(
                                "Sharpe Ratio",
                                f"{metrics['sharpe_ratio']:.2f}"
                            )

                        with col4:

                            st.metric(
                                "Max Drawdown",
                                f"{metrics['max_drawdown'] * 100:.2f}%"
                            )

                        # ------------------------------------
                        # Sortino + Diversification
                        # ------------------------------------

                        col5, col6 = st.columns(2)

                        with col5:

                            st.metric(
                                "Sortino Ratio",
                                f"{metrics['sortino_ratio']:.2f}"
                            )

                        with col6:

                            st.metric(
                                "Diversification Score",
                                f"{diversification_score:.1f}/100"
                            )

                        # ------------------------------------
                        # Allocation Table
                        # ------------------------------------

                        st.markdown(
                            "### 🧾 Portfolio Allocation"
                        )

                        allocation_df = (
                            build_portfolio_summary(
                                selected_funds,
                                weights,
                                metrics,
                                diversification_score
                            )
                        )

                        allocation_df[
                            "Weight"
                        ] = allocation_df[
                            "Weight"
                        ].map(
                            lambda x: f"{x:.2f}%"
                        )

                        st.dataframe(
                            allocation_df,
                            width="stretch",
                            hide_index=True
                        )

                        # ------------------------------------
                        # Correlation Matrix
                        # ------------------------------------

                        st.markdown(
                            "### 🔗 Fund Correlation Matrix"
                        )

                        correlation_matrix = (
                            returns_matrix.corr()
                        )

                        st.dataframe(
                            correlation_matrix.round(2),
                            width="stretch"
                        )

                        # ------------------------------------
                        # Portfolio Return Contribution
                        # ------------------------------------

                        st.markdown(
                            "### 📈 Return Contribution"
                        )

                        individual_returns = (
                            returns_matrix.mean()
                            * 252
                            * 100
                        )

                        contribution_df = pd.DataFrame({
                            "Fund": selected_funds,
                            "Allocation (%)": (
                                weights * 100
                            ),
                            "Annualized Return (%)": [
                                individual_returns.get(
                                    fund,
                                    0
                                )
                                for fund in selected_funds
                            ]
                        })

                        contribution_df[
                            "Return Contribution (%)"
                        ] = (
                            contribution_df[
                                "Allocation (%)"
                            ]
                            *
                            contribution_df[
                                "Annualized Return (%)"
                            ]
                            / 100
                        )

                        st.dataframe(
                            contribution_df.round(2),
                            width="stretch",
                            hide_index=True
                        )

                except Exception as e:

                    st.error(
                        f"Unable to analyze portfolio: {e}"
                    )