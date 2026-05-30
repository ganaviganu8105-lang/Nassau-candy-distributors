import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processing import (
    load_data,
    cost_structure_analysis,
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

    .warning-box {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.3);
        border-radius: 12px;
        padding: 16px 20px;
        color: #ffaaaa;
        font-size: 0.95em;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# PAGE HEADER
# -----------------------------
st.markdown("""
<div class="page-header">
    <h1>💰 Cost vs Margin Diagnostics</h1>
    <p>Identify cost-heavy products, pricing inefficiencies and discontinuation candidates</p>
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
# COST ANALYSIS
# -----------------------------
cost_df = cost_structure_analysis(filtered_df)

# -----------------------------
# SCATTER: COST vs SALES
# -----------------------------
st.markdown('<div class="section-title">📊 Cost vs Sales Analysis</div>', unsafe_allow_html=True)

fig1 = px.scatter(
    filtered_df,
    x="Cost",
    y="Sales",
    color="Division",
    hover_data=["Product Name"],
    template="plotly_dark",
    color_discrete_sequence=["#FFD700", "#ff6b6b", "#4ecdc4"],
    labels={
        "Cost": "Cost ($)",
        "Sales": "Sales ($)"
    }
)
fig1.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.03)",
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -----------------------------
# PRICING ISSUE PRODUCTS
# -----------------------------
st.markdown('<div class="section-title">⚠️ Pricing Inefficiency — High Sales but Low Profit</div>', unsafe_allow_html=True)

pricing_issue = cost_df[cost_df["Pricing Issue"] == True]

if pricing_issue.empty:
    st.markdown('<div class="info-box">✅ No pricing inefficiency products found with current filters.</div>', unsafe_allow_html=True)
else:
    st.dataframe(pricing_issue, use_container_width=True)

st.markdown("---")

# -----------------------------
# COST HEAVY PRODUCTS
# -----------------------------
st.markdown('<div class="section-title">🚨 Cost Heavy Products</div>', unsafe_allow_html=True)

cost_heavy = cost_df[cost_df["Cost Heavy"] == True]

if cost_heavy.empty:
    st.markdown('<div class="info-box">✅ No cost heavy products found with current filters.</div>', unsafe_allow_html=True)
else:
    st.dataframe(cost_heavy, use_container_width=True)

st.markdown("---")

# -----------------------------
# DISCONTINUE SUGGESTION
# -----------------------------
st.markdown('<div class="section-title">❌ Products for Discontinuation Review</div>', unsafe_allow_html=True)

discontinue = cost_df[cost_df["Discontinue Review"] == True]

if discontinue.empty:
    st.markdown('<div class="info-box">✅ No products flagged for discontinuation with current filters.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="warning-box">⚠️ These products have high cost ratios and low sales. Consider repricing or discontinuing.</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.dataframe(discontinue, use_container_width=True)
