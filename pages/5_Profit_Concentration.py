import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_processing import (
    load_data,
    pareto_analysis,
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

    .kpi-value-red {
        font-size: 1.9em;
        font-weight: 800;
        color: #ff6b6b;
    }

    .section-title {
        font-size: 1.2em;
        font-weight: 700;
        color: #FFD700;
        margin: 25px 0 12px 0;
        border-left: 5px solid #FFD700;
        padding-left: 12px;
    }

    .risk-box {
        background: rgba(255, 107, 107, 0.1);
        border: 1px solid rgba(255, 107, 107, 0.35);
        border-radius: 12px;
        padding: 16px 20px;
        color: #ffaaaa;
        font-size: 1em;
        font-weight: 600;
    }

    .safe-box {
        background: rgba(46, 204, 113, 0.1);
        border: 1px solid rgba(46, 204, 113, 0.35);
        border-radius: 12px;
        padding: 16px 20px;
        color: #aaffcc;
        font-size: 1em;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# PAGE HEADER
# -----------------------------
st.markdown("""
<div class="page-header">
    <h1>📈 Profit Concentration Analysis</h1>
    <p>Pareto (80/20) analysis — find the few products driving most of the profit</p>
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
# PARETO ANALYSIS
# -----------------------------
pareto_df = pareto_analysis(filtered_df)
pareto_df = pareto_df.head(20)

# -----------------------------
# DEPENDENCY KPI CARDS
# -----------------------------
top_80 = pareto_df[pareto_df["Cumulative Profit %"] <= 80]
num_products = len(top_80)
total_products = len(pareto_df)
dependency_ratio = (num_products / total_products * 100) if total_products > 0 else 0

st.markdown('<div class="section-title">📌 Profit Concentration KPIs</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📦</div>
        <div class="kpi-label">Total Products</div>
        <div class="kpi-value">{total_products}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🏆</div>
        <div class="kpi-label">Products → 80% Profit</div>
        <div class="kpi-value">{num_products}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-label">Dependency Ratio</div>
        <div class="kpi-value-red">{dependency_ratio:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")

# -----------------------------
# PARETO CHART
# -----------------------------
st.markdown('<div class="section-title">📊 Pareto Chart — 80/20 Rule</div>', unsafe_allow_html=True)

fig = go.Figure()

# Profit bars
fig.add_trace(go.Bar(
    x=pareto_df["Product Name"],
    y=pareto_df["Profit"],
    name="Profit",
    marker_color="#FFD700",
    opacity=0.85
))

# Cumulative % line
fig.add_trace(go.Scatter(
    x=pareto_df["Product Name"],
    y=pareto_df["Cumulative Profit %"],
    name="Cumulative %",
    yaxis="y2",
    line=dict(color="#ff6b6b", width=2.5),
    mode="lines+markers",
    marker=dict(size=6)
))

# 80% reference line
fig.add_hline(
    y=80,
    line_dash="dash",
    line_color="#4ecdc4",
    annotation_text="80% Threshold",
    annotation_position="top left",
    yref="y2"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.03)",
    xaxis_title="Product",
    yaxis_title="Profit ($)",
    yaxis2=dict(
        title="Cumulative Profit %",
        overlaying="y",
        side="right",
        range=[0, 110]
    ),
    showlegend=True,
    xaxis_tickangle=-45,
    height=500,
    margin=dict(t=40, b=180),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# -----------------------------
# RISK INDICATOR
# -----------------------------
st.markdown('<div class="section-title">⚠️ Dependency Risk Indicator</div>', unsafe_allow_html=True)

if num_products < (0.3 * total_products):
    st.markdown(f'<div class="risk-box">🚨 High Dependency Risk — Only {num_products} out of {total_products} products contribute 80% of profit. Business is over-reliant on very few products!</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="safe-box">✅ Balanced Distribution — {num_products} out of {total_products} products contribute 80% of profit. Profit is well spread across the portfolio.</div>', unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# FULL TABLE
# -----------------------------
st.markdown('<div class="section-title">📋 Product Profit Contribution Table</div>', unsafe_allow_html=True)

pareto_display = pareto_df[["Product Name", "Sales", "Profit", "Cumulative Profit %"]].copy()
pareto_display["Sales"] = pareto_display["Sales"].map("${:,.0f}".format)
pareto_display["Profit"] = pareto_display["Profit"].map("${:,.0f}".format)
pareto_display["Cumulative Profit %"] = pareto_display["Cumulative Profit %"].map("{:.1f}%".format)

st.dataframe(pareto_display, use_container_width=True)
