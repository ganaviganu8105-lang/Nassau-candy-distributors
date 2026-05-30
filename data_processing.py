import pandas as pd

# ======================================
# STEP 1: LOAD + CLEAN DATA
# ======================================
def load_and_clean_data(filename="Nassau.csv"):
    df = pd.read_csv(filename)

    # Remove missing critical values
    df = df.dropna(subset=["Sales", "Cost"])

    # Remove invalid values
    df = df[df["Sales"] > 0]
    df = df[df["Units"] > 0]

    # Fill missing cost
    df["Cost"] = df["Cost"].fillna(0)

    # Clean text columns
    df["Product Name"] = df["Product Name"].str.strip()
    df["Division"] = df["Division"].str.strip()

    return df


# ======================================
# STEP 2: CALCULATE METRICS
# ======================================
def calculate_metrics(df):

    df["Profit"] = df["Sales"] - df["Cost"]

    df["Gross Margin %"] = (df["Profit"] / df["Sales"]) * 100
    df["Gross Margin %"] = df["Gross Margin %"].fillna(0)

    df["Cost per Unit"] = df["Cost"] / df["Units"]
    df["Profit per Unit"] = df["Profit"] / df["Units"]

    df["Cost per Unit"] = df["Cost per Unit"].fillna(0)
    df["Profit per Unit"] = df["Profit per Unit"].fillna(0)

    return df


# ======================================
# STEP 3: PRODUCT LEVEL ANALYSIS
# ======================================
def product_level_analysis(df):

    product_df = df.groupby("Product Name").agg({
        "Sales": "sum",
        "Cost": "sum",
        "Profit": "sum"
    }).reset_index()

    product_df["Gross Margin %"] = (product_df["Profit"] / product_df["Sales"]) * 100
    product_df["Gross Margin %"] = product_df["Gross Margin %"].fillna(0)

    product_df = product_df.sort_values(by="Profit", ascending=False)

    profit_threshold = product_df["Profit"].quantile(0.7)
    margin_threshold = product_df["Gross Margin %"].quantile(0.7)
    low_sales_threshold = product_df["Sales"].quantile(0.3)

    def classify(row):
        if row["Profit"] >= profit_threshold and row["Gross Margin %"] >= margin_threshold:
            return "High Profit & High Margin"
        elif row["Sales"] >= product_df["Sales"].quantile(0.7) and row["Gross Margin %"] < margin_threshold:
            return "High Sales but Low Margin"
        elif row["Sales"] <= low_sales_threshold and row["Profit"] <= product_df["Profit"].quantile(0.3):
            return "Low Sales & Low Profit"
        else:
            return "Average"

    product_df["Category"] = product_df.apply(classify, axis=1)

    return product_df


# ======================================
# STEP 4: PARETO ANALYSIS
# ======================================
def pareto_analysis(df):

    pareto_df = df.groupby("Product Name").agg({
        "Sales": "sum",
        "Profit": "sum"
    }).reset_index()

    pareto_df = pareto_df.sort_values(by="Profit", ascending=False)

    pareto_df["Cumulative Profit"] = pareto_df["Profit"].cumsum()
    total_profit = pareto_df["Profit"].sum()

    if total_profit != 0:
        pareto_df["Cumulative Profit %"] = (pareto_df["Cumulative Profit"] / total_profit) * 100
    else:
        pareto_df["Cumulative Profit %"] = 0

    return pareto_df


# ======================================
# STEP 5: COST ANALYSIS
# ======================================
def cost_structure_analysis(df):

    cost_df = df.groupby("Product Name").agg({
        "Sales": "sum",
        "Cost": "sum",
        "Profit": "sum"
    }).reset_index()

    cost_df["Cost Ratio"] = cost_df["Cost"] / cost_df["Sales"]

    # Use data-driven threshold (top 40% cost ratio = cost heavy)
    cost_ratio_threshold = cost_df["Cost Ratio"].quantile(0.6)

    cost_df["Cost Heavy"] = (
        (cost_df["Cost Ratio"] >= cost_ratio_threshold) &
        (cost_df["Profit"] < cost_df["Profit"].mean())
    )

    cost_df["Low Margin"] = cost_df["Profit"] < cost_df["Profit"].mean()

    cost_df["Pricing Issue"] = (
        (cost_df["Sales"] > cost_df["Sales"].median()) &
        (cost_df["Profit"] < cost_df["Profit"].median())
    )

    cost_df["Discontinue Review"] = (
        (cost_df["Cost Ratio"] >= cost_ratio_threshold) &
        (cost_df["Sales"] < cost_df["Sales"].mean())
    )

    return cost_df


# ======================================
# STEP 6: KPI CALCULATIONS
# ======================================
def calculate_kpis(df):

    kpi = {}

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_units = df["Units"].sum()

    kpi["Gross Margin (%)"] = (total_profit / total_sales) * 100 if total_sales != 0 else 0
    kpi["Profit per Unit"] = total_profit / total_units if total_units != 0 else 0

    revenue_by_product = df.groupby("Product Name")["Sales"].sum()
    profit_by_product = df.groupby("Product Name")["Profit"].sum()

    kpi["Top Product Revenue Contribution (%)"] = (
        (revenue_by_product.max() / total_sales) * 100 if total_sales != 0 else 0
    )

    kpi["Top Product Profit Contribution (%)"] = (
        (profit_by_product.max() / total_profit) * 100 if total_profit != 0 else 0
    )

    margin = (df["Profit"] / df["Sales"]).replace(
        [float('inf'), -float('inf')], 0
    ).fillna(0)

    kpi["Margin Volatility"] = margin.std()

    return kpi


# ======================================
# STEP 7: FILTERS
# ======================================
def apply_filters(df, division=None, margin_threshold=None, product_search=None):

    filtered_df = df.copy()

    if division:
        filtered_df = filtered_df[filtered_df["Division"].isin(division)]

    if margin_threshold is not None:
        filtered_df["Margin"] = filtered_df["Profit"] / filtered_df["Sales"]
        filtered_df = filtered_df[filtered_df["Margin"] >= margin_threshold]

    if product_search:
        filtered_df = filtered_df[
            filtered_df["Product Name"].str.contains(product_search, case=False, na=False)
        ]

    return filtered_df


# ======================================
# MAIN FUNCTION
# ======================================
def load_data(filename="Nassau.csv"):
    df = load_and_clean_data(filename)
    df = calculate_metrics(df)
    return df
