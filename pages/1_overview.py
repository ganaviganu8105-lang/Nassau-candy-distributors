import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processing import (
    load_data,
    calculate_kpis,
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
        background-color: #f9f9f9;
    }

    .page-header {
        background: linear-gradient(120deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 16px;
        padding: 30px 40px;
        margin-bottom: 30px;
        text-align: center;
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

    /* KPI Cards */
    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 24px 20px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-top: 5px solid #FFD700;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }

    .kpi-icon {
        font-size: 2em;
        margin-bottom: 8px;
    }

    .kpi-label {
        font-size: 0.85em;
        color: #888;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    .kpi-value {
        font-size: 2em;
        font-weight: 800;
        color: #1a1a2e;
    }

    .kpi-value-green {
        font-size: 2em;
        font-weight: 800;
        color: #27ae60;
    }

    .kpi-value-blue {
        font-size: 2em;
        font-weight: 800;
        color: #2980b9;
    }

    .section-title {
        font-size: 1.3em;
        font-weight: 700;
        color: #1a1a2e;
        margin: 30px 0 15px 0;
        border-left: 5px solid #FFD700;
        padding-left: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# PAGE HEADER
# -----------------------------
st.markdown("""
<div class="page-header">
    <h1>📊 Overview Dashboard</h1>
    <p>High-level profitability summary across all products and divisions</p>
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

product_search = st.sidebar.text_input("🔍 Search Product")

# Apply filters
filtered_df = apply_filters(
    df,
    division=division,
    margin_threshold=margin_threshold,
    product_search=product_search
)

# -----------------------------
# KPI SECTION
# -----------------------------
st.markdown('<div class="section-title">📌 Key Performance Indicators</div>', unsafe_allow_html=True)

kpi = calculate_kpis(filtered_df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💵</div>
        <div class="kpi-label">Total Sales</div>
        <div class="kpi-value">${filtered_df['Sales'].sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Total Profit</div>
        <div class="kpi-value-green">${filtered_df['Profit'].sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📈</div>
        <div class="kpi-label">Avg Gross Margin</div>
        <div class="kpi-value-blue">{kpi['Gross Margin (%)']:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📦</div>
        <div class="kpi-label">Total Units</div>
        <div class="kpi-value">{filtered_df['Units'].sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# DIVISION PERFORMANCE
# -----------------------------
st.markdown('<div class="section-title">📦 Division Performance</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    sales_div = filtered_df.groupby("Division")["Sales"].sum().reset_index()
    fig1 = px.bar(
        sales_div, x="Division", y="Sales", color="Division",
        template="plotly_white",
        title="Sales by Division",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    profit_div = filtered_df.groupby("Division")["Profit"].sum().reset_index()
    fig2 = px.bar(
        profit_div, x="Division", y="Profit", color="Division",
        template="plotly_white",
        title="Profit by Division",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# PROFIT DISTRIBUTION & TOP 10
# -----------------------------
st.markdown('<div class="section-title">🏆 Product Insights</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig3 = px.histogram(
        filtered_df, x="Profit", nbins=30,
        template="plotly_white",
        title="Profit Distribution",
        color_discrete_sequence=["#FFD700"]
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    top_products = (
        filtered_df.groupby("Product Name")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig4 = px.bar(
        top_products, x="Profit", y="Product Name",
        orientation="h",
        template="plotly_white",
        title="Top 10 Products by Profit",
        color="Profit",
        color_continuous_scale="YlOrRd"
    )
    fig4.update_yaxes(categoryorder="total ascending")
    fig4.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)
