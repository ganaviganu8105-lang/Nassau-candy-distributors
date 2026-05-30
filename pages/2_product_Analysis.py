import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processing import (
    load_data,
    product_level_analysis,
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
    <h1>🏆 Product Analysis Dashboard</h1>
    <p>Deep dive into product-level profitability and margin performance</p>
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
# PRODUCT LEVEL ANALYSIS
# -----------------------------
product_df = product_level_analysis(filtered_df)

# -----------------------------
# TOP PRODUCTS BY PROFIT
# -----------------------------
st.markdown('<div class="section-title">🏆 Top 10 Products by Profit</div>', unsafe_allow_html=True)

top_profit = product_df.head(10)

fig1 = px.bar(
    top_profit,
    x="Profit",
    y="Product Name",
    orientation="h",
    color="Profit",
    color_continuous_scale="YlOrRd",
    template="plotly_dark"
)
fig1.update_yaxes(categoryorder="total ascending")
fig1.update_layout(
    coloraxis_showscale=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -----------------------------
# TOP PRODUCTS BY MARGIN
# -----------------------------
st.markdown('<div class="section-title">📈 Top Products by Gross Margin %</div>', unsafe_allow_html=True)

top_margin = product_df.sort_values(by="Gross Margin %", ascending=False).head(10)

fig2 = px.bar(
    top_margin,
    x="Gross Margin %",
    y="Product Name",
    orientation="h",
    color="Gross Margin %",
    color_continuous_scale="Teal",
    template="plotly_dark"
)
fig2.update_yaxes(categoryorder="total ascending")
fig2.update_layout(
    coloraxis_showscale=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# PRODUCT CLASSIFICATION
# -----------------------------
st.markdown('<div class="section-title">📊 Product Performance Classification</div>', unsafe_allow_html=True)

fig3 = px.histogram(
    product_df,
    x="Category",
    color="Category",
    template="plotly_dark",
    color_discrete_sequence=["#FFD700", "#ff6b6b", "#4ecdc4", "#95e1d3"]
)
fig3.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    showlegend=False
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# -----------------------------
# HIGH SALES BUT LOW MARGIN
# -----------------------------
st.markdown('<div class="section-title">⚠️ High Sales but Low Margin Products</div>', unsafe_allow_html=True)

problem_products = product_df[product_df["Category"] == "High Sales but Low Margin"]

if problem_products.empty:
    st.markdown('<div class="info-box">✅ No high sales / low margin products found with current filters.</div>', unsafe_allow_html=True)
else:
    st.dataframe(problem_products, use_container_width=True)
