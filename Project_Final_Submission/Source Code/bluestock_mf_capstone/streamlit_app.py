import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# ==========================================
# 1. PAGE CONFIG & PREMIUM CSS
# ==========================================
st.set_page_config(page_title="Bluestock Pro Analytics", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b101a; color: #e2e8f0; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #121826; border-right: 1px solid #1e293b; }
    [data-testid="stMetricValue"] { color: #38bdf8; font-size: 2rem; font-weight: 700; }
    [data-testid="stMetricLabel"] { color: #94a3b8; font-size: 1.1rem; font-weight: 500; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; border-bottom: 1px solid #1e293b; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: transparent; color: #94a3b8; font-weight: 600; font-size: 1.1rem; padding: 0 20px; border: none; }
    .stTabs [aria-selected="true"] { color: #ffffff; border-bottom: 3px solid #38bdf8; background-color: rgba(56, 189, 248, 0.1); border-radius: 5px 5px 0 0; }
    h1, h2, h3 { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. HEADER SECTION
# ==========================================
col_logo, col_title = st.columns([1, 15])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/2933/2933116.png", width=60)
with col_title:
    st.markdown("<h1 style='margin-bottom: 0px; padding-bottom: 0px; line-height: 1.2;'>Bluestock Analytics Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 1.1rem;'>Institutional-Grade Mutual Fund Performance Tracker & Macro Trends</p>", unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #1e293b; margin-top: 5px;'>", unsafe_allow_html=True)

# ==========================================
# 3. DATA ENGINE (Absolute Path Fix)
# ==========================================
@st.cache_data
def get_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, 'data', 'db', 'bluestock_mf.db')
    
    conn = sqlite3.connect(db_path)
    
    query_nav = """
    SELECT n.nav_date, n.nav, n.amfi_code, f.scheme_name, f.category 
    FROM fact_nav n
    JOIN dim_fund f ON n.amfi_code = f.amfi_code
    """
    try:
        df_nav = pd.read_sql_query(query_nav, conn)
    except:
        df_nav = pd.read_sql_query("SELECT * FROM fact_nav", conn)
        df_nav['scheme_name'] = df_nav['amfi_code'].astype(str)
        
    try:
        df_sip = pd.read_sql_query("SELECT * FROM fact_sip_industry", conn)
    except:
        sip_path = os.path.join(BASE_DIR, 'data', 'raw', '04_monthly_sip_inflows.csv')
        if os.path.exists(sip_path):
            df_sip = pd.read_csv(sip_path)
        else:
            df_sip = pd.DataFrame()

    try:
        df_aum = pd.read_sql_query("SELECT * FROM fact_aum", conn)
    except:
        aum_path = os.path.join(BASE_DIR, 'data', 'raw', '03_aum_by_fund_house.csv')
        if os.path.exists(aum_path):
            df_aum = pd.read_csv(aum_path)
        else:
            df_aum = pd.DataFrame()
            
    conn.close()
    
    df_nav['nav_date'] = pd.to_datetime(df_nav['nav_date'])
    return df_nav, df_sip, df_aum

df_nav, df_sip, df_aum = get_data()

# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================
st.sidebar.markdown("<h3 style='color: #ffffff;'>Filter Parameters</h3>", unsafe_allow_html=True)
scheme_list = df_nav['scheme_name'].unique()
selected_scheme = st.sidebar.selectbox("Select Asset / Mutual Fund Scheme", scheme_list)

min_date = df_nav['nav_date'].min().date()
max_date = df_nav['nav_date'].max().date()

st.sidebar.markdown("<hr style='border: 1px solid #1e293b;'>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='color: #94a3b8;'>Date Range</h4>", unsafe_allow_html=True)
try:
    start_date, end_date = st.sidebar.date_input(
        "Select Trading Period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
except ValueError:
    st.sidebar.error("Please select both start and end dates.")
    start_date, end_date = min_date, max_date

filtered_data = df_nav[
    (df_nav['scheme_name'] == selected_scheme) & 
    (df_nav['nav_date'].dt.date >= start_date) & 
    (df_nav['nav_date'].dt.date <= end_date)
].sort_values(by='nav_date')

# ==========================================
# 5. INTERACTIVE TABS & LAYOUT
# ==========================================
tab1, tab2 = st.tabs(["Fund Performance", "Macro Industry Trends"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    if not filtered_data.empty:
        latest_date = filtered_data['nav_date'].max()
        latest_nav = filtered_data[filtered_data['nav_date'] == latest_date]['nav'].values[0]
        total_records = len(filtered_data)

        with col1:
            st.metric(label="Latest Net Asset Value (NAV)", value=f"₹ {latest_nav:.2f}")
        with col2:
            st.metric(label="Last Updated", value=str(latest_date.date()))
        with col3:
            st.metric(label="Trading Days Captured", value=total_records)

        st.markdown("<hr style='border: 1px solid #1e293b; margin: 20px 0;'>", unsafe_allow_html=True)

        chart_col, table_col = st.columns([2.8, 1.2])

        with chart_col:
            st.markdown(f"<h4 style='color: #e2e8f0;'>Historical NAV Trajectory</h4>", unsafe_allow_html=True)
            
            fig_nav = px.area(filtered_data, x='nav_date', y='nav', title="")
            fig_nav.update_traces(line_color='#38bdf8', fillcolor='rgba(56, 189, 248, 0.1)')
            fig_nav.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, title=""),
                yaxis=dict(showgrid=True, gridcolor='#1e293b', title="NAV (₹)"),
                margin=dict(l=0, r=0, t=10, b=0)
            )
            st.plotly_chart(fig_nav, use_container_width=True)

        with table_col:
            st.markdown(f"<h4 style='color: #e2e8f0;'>Recent Data Log</h4>", unsafe_allow_html=True)
            recent_data = filtered_data[['nav_date', 'nav']].sort_values(by='nav_date', ascending=False).head(15)
            recent_data['nav_date'] = recent_data['nav_date'].dt.strftime('%Y-%m-%d')
            st.dataframe(recent_data, use_container_width=True, hide_index=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            csv = filtered_data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Data (CSV)",
                data=csv,
                file_name=f"{selected_scheme}_data.csv",
                mime='text/csv',
                use_container_width=True
            )
    else:
        st.warning("No data available for the selected date range. Please adjust the calendar filter.")

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_sip, col_aum = st.columns(2)

    with col_sip:
        if not df_sip.empty:
            st.markdown(f"<h4 style='color: #e2e8f0;'>Monthly SIP Inflows</h4>", unsafe_allow_html=True)
            x_col, y_col = df_sip.columns[0], df_sip.columns[1]
            fig_sip = px.bar(df_sip, x=x_col, y=y_col)
            fig_sip.update_traces(marker_color='#f59e0b')
            fig_sip.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, title="Month"), yaxis=dict(showgrid=True, gridcolor='#1e293b', title="Inflow (Cr)"),
                margin=dict(l=0, r=0, t=10, b=0)
            )
            st.plotly_chart(fig_sip, use_container_width=True)
        else:
            st.info("SIP Inflow data not available.")

    with col_aum:
        if not df_aum.empty:
            st.markdown(f"<h4 style='color: #e2e8f0;'>Top Fund Houses by AUM</h4>", unsafe_allow_html=True)
            x_col, y_col = df_aum.columns[0], df_aum.columns[2]
            aum_agg = df_aum.groupby(x_col)[y_col].max().reset_index().sort_values(by=y_col, ascending=False).head(10)
            fig_aum = px.bar(aum_agg, x=x_col, y=y_col)
            fig_aum.update_traces(marker_color='#10b981')
            fig_aum.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, title="Asset Management Company"), yaxis=dict(showgrid=True, gridcolor='#1e293b', title="AUM (Cr)"),
                margin=dict(l=0, r=0, t=10, b=0)
            )
            st.plotly_chart(fig_aum, use_container_width=True)
        else:
            st.info("AUM data not available.")