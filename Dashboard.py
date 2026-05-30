import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Nassau Candy Dashboard",
    page_icon="🍬",
    layout="wide"
)

# =========================
# CUSTOM CSS - Clean & Light
# =========================
st.markdown("""
    <style>

    /* Clean white background */
    .stApp {
        background-color: #f9f9f9;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(120deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 20px;
        padding: 50px 40px;
        text-align: center;
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 2.8em;
        font-weight: 900;
        color: #FFD700;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .hero-sub {
        font-size: 1.1em;
        color: #cccccc;
    }

    /* Section heading */
    .section-title {
        font-size: 1.4em;
        font-weight: 700;
        color: #1a1a2e;
        margin: 30px 0 15px 0;
        border-left: 5px solid #FFD700;
        padding-left: 12px;
    }

    /* Feature cards */
    .feat-card {
        background: white;
        border-radius: 14px;
        padding: 22px 18px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-top: 4px solid #FFD700;
        height: 100%;
        transition: box-shadow 0.2s;
    }

    .feat-card:hover {
        box-shadow: 0 6px 24px rgba(0,0,0,0.15);
    }

    .feat-icon {
        font-size: 2em;
        margin-bottom: 10px;
    }

    .feat-title {
        font-size: 1em;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 6px;
    }

    .feat-desc {
        font-size: 0.88em;
        color: #666666;
        line-height: 1.5;
    }

    /* Nav cards */
    .nav-card {
        background: white;
        border: 1.5px solid #e0e0e0;
        border-left: 5px solid #FFD700;
        border-radius: 10px;
        padding: 14px 18px;
        margin: 8px 0;
        font-size: 0.95em;
        font-weight: 600;
        color: #1a1a2e;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    }

    /* Badge */
    .badge {
        display: inline-block;
        background: #1a1a2e;
        color: #FFD700;
        border-radius: 20px;
        padding: 5px 16px;
        font-size: 0.85em;
        font-weight: 600;
        margin: 4px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.82em;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e0e0e0;
    }

    </style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-title">🍬 Nassau Candy Distributor</div>
    <div class="hero-sub">Product Line Profitability & Margin Performance Dashboard</div>
</div>
""", unsafe_allow_html=True)

# =========================
# FEATURE CARDS
# =========================
st.markdown('<div class="section-title">📊 What This Dashboard Provides</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feat-card">
        <div class="feat-icon">🏆</div>
        <div class="feat-title">Product Profitability</div>
        <div class="feat-desc">Identify top and bottom performing products by profit and margin</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feat-card">
        <div class="feat-icon">🏢</div>
        <div class="feat-title">Division Performance</div>
        <div class="feat-desc">Compare revenue vs profit across all product divisions</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feat-card">
        <div class="feat-icon">💰</div>
        <div class="feat-title">Cost Diagnostics</div>
        <div class="feat-desc">Spot pricing inefficiencies and cost-heavy products</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feat-card">
        <div class="feat-icon">📈</div>
        <div class="feat-title">Pareto Analysis</div>
        <div class="feat-desc">Discover which few products drive 80% of total profit</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# NAVIGATION SECTION
# =========================
st.markdown('<div class="section-title">📂 Navigate Using the Sidebar</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="nav-card">📊 &nbsp; 1 — Overview Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-card">🏆 &nbsp; 2 — Product Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-card">🏢 &nbsp; 3 — Division Performance</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="nav-card">💰 &nbsp; 4 — Cost Diagnostics</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-card">📈 &nbsp; 5 — Profit Concentration</div>', unsafe_allow_html=True)

# =========================
# BUILT WITH
# =========================
st.markdown('<div class="section-title">🚀 Built With</div>', unsafe_allow_html=True)

st.markdown("""
<span class="badge">🐍 Python</span>
<span class="badge">📊 Streamlit</span>
<span class="badge">🐼 Pandas</span>
<span class="badge">📉 Plotly</span>
""", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    Developed for Data Analytics Project &nbsp;|&nbsp; Nassau Candy Distributor &nbsp;|&nbsp; 2025
</div>
""", unsafe_allow_html=True)
