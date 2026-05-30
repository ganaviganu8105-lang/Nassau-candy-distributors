import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processing import (
    load_data,
    apply_filters
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #1a1a2e;
    }

    .page-header {
        background: linear-gradient(120deg, #16213e, #0f3460);
        border-radius: 16px;
        padding: 30px 40px;
        margin-bottom: 30px;
        text-align: center;
        border: 1px solid rgba(255,215,0,0.2);
    }

    .page-header h1 {
        color: #FFD700;
        font-size: 2.2em;
        font-weight: 800;
        margin: 0;
    }

    .page-header p {
        color: #cccccc;
        font-size: 1em;
        margin-top: 6px;
    }

    .kpi-card {
        background: linear-gradient(135deg, #16213e, #0f3460);
        border-radius: 14px;
        padding: 24px 20px;
        text-align: center;
        border: 1px solid rgba(255,215,0,0.25);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }

    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(255,215,0,0.15);
    }

    .kpi-icon {
        font-size: 2em;
        margin-bottom: 8px;
    }

    .kpi-label {
        font-size: 0.8em;
        color: #aaaaaa;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 1.9em;
        font-weight: 800;
        color: #FFD700;
    }

    .kpi-value-green {
        font-size: 1.9em;
        font-weight: 800;
        color: #2ecc71;
    }

    .kpi-value-blue {
        font-size: 1.9em;
        font-weight: 800;
        color: #3498db;
    }

    .section-title {
        font-size: 1.2em;
        font-weight: 700;
        color: #FFD700;
        margin: 25px 0 12px 0;
        border-left: 5px solid #FFD700;
        padding-left: 12px;
    }

    .info-box {
        background: rgba(255,215,0,0.08);
        border: 1px solid rgba(255,215,0,0.2);
        border-radius: 12px;
        padding: 16px 20px;
        color: #cccccc;
        font-size: 0.95em;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# PAGE HEADER
# -----------------------------
st.markdown("""
<div class="page-header">
    <h1>🏢 Division Performance Dashboard</h1>
    <p>Revenue vs profit comparison across all product divisions</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_data("Nassau.csv")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔧 Filters")

division = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=list(df["Division"].unique())
)

margin_threshold = st.sidebar.slider(
    "Minimum Margin (%)",
    0, 100, 0
) / 100

# Apply filters
filtered_df = apply_filters(
    df,
    division=division,
    margin_threshold=margin_threshold
)

# -----------------------------
# DIVISION AGGREGATION
# -----------------------------
division_df = filtered_df.groupby("Division").agg({
    "Sales": "sum",
    "Profit": "sum"
}).reset_index()

division_df["Margin %"] = (division_df["Profit"] / division_df["Sales"]) * 100
division_df["Margin %"] = division_df["Margin %"].fillna(0)

# -----------------------------
# KPI CARDS
# -----------------------------
st.markdown('<div class="section-title">📌 Division KPIs</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💵</div>
        <div class="kpi-label">Total Sales</div>
        <div class="kpi-value">${division_df['Sales'].sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Total Profit</div>
        <div class="kpi-value-green">${division_df['Profit'].sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📈</div>
        <div class="kpi-label">Avg Margin</div>
        <div class="kpi-value-blue">{division_df['Margin %'].mean():.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# REVENUE vs PROFIT
# -----------------------------
st.markdown('<div class="section-title">📊 Revenue vs Profit by Division</div>', unsafe_allow_html=True)

fig1 = px.bar(
    division_df,
    x="Division",
    y=["Sales", "Profit"],
    barmode="group",
    template="plotly_dark",
    color_discrete_map={"Sales": "#FFD700", "Profit": "#2ecc71"}
)
fig1.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend_title_text=""
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -----------------------------
# MARGIN DISTRIBUTION
# -----------------------------
st.markdown('<div class="section-title">📈 Margin % by Division</div>', unsafe_allow_html=True)

fig2 = px.bar(
    division_df,
    x="Division",
    y="Margin %",
    color="Division",
    template="plotly_dark",
    color_discrete_sequence=["#FFD700", "#ff6b6b", "#4ecdc4"]
)
fig2.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# SUMMARY TABLE
# -----------------------------
st.markdown('<div class="section-title">📋 Division Summary Table</div>', unsafe_allow_html=True)

if division_df.empty:
    st.markdown('<div class="info-box">No data available with current filters.</div>', unsafe_allow_html=True)
else:
    st.dataframe(
        division_df.sort_values(by="Profit", ascending=False),
        use_container_width=True
    )
