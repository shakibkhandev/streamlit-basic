import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Advanced Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Generate More Detailed Dummy Data
@st.cache_data
def load_data():
    np.random.seed(42)
    
    # Create date range
    dates = pd.date_range("2024-01-01", periods=90)
    
    # Define categories
    regions = ["North", "South", "East", "West"]
    products = ["Chai", "Coffee", "Green Tea", "Black Tea", "Herbal Tea"]
    channels = ["Online", "Retail", "Wholesale"]
    
    # Generate data with more features
    data = {
        "Date": np.repeat(dates, 20),
        "Region": np.random.choice(regions, size=1800),
        "Product": np.random.choice(products, size=1800),
        "Channel": np.random.choice(channels, size=1800),
        "Revenue": np.random.randint(500, 5000, 1800),
        "Units_Sold": np.random.randint(10, 200, 1800),
        "Customer_Rating": np.random.uniform(3.5, 5.0, 1800).round(1),
        "Cost": np.random.randint(200, 2000, 1800)
    }
    
    df = pd.DataFrame(data)
    df["Profit"] = df["Revenue"] - df["Cost"]
    df["Profit_Margin"] = (df["Profit"] / df["Revenue"] * 100).round(2)
    
    return df

# Load Data
df = load_data()

# Sidebar Filters
st.sidebar.title("📊 Dashboard Filters")

# Date Filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["Date"].min(), df["Date"].max()),
    min_value=df["Date"].min(),
    max_value=df["Date"].max()
)

# Other Filters
region_filter = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
product_filter = st.sidebar.multiselect("Select Product", df["Product"].unique(), default=df["Product"].unique())
channel_filter = st.sidebar.multiselect("Select Channel", df["Channel"].unique(), default=df["Channel"].unique())

# Apply Filters
filtered_df = df[
    (df["Date"].dt.date >= date_range[0]) &
    (df["Date"].dt.date <= date_range[1]) &
    (df["Region"].isin(region_filter)) &
    (df["Product"].isin(product_filter)) &
    (df["Channel"].isin(channel_filter))
]

# Main Dashboard
st.title("📈 Advanced Sales Analytics Dashboard")
st.markdown("Interactive dashboard showing key sales metrics and trends")

# Top KPIs
col1, col2, col3, col4 = st.columns(4)

# Calculate KPI metrics
total_revenue = filtered_df["Revenue"].sum()
total_profit = filtered_df["Profit"].sum()
avg_margin = filtered_df["Profit_Margin"].mean()
avg_rating = filtered_df["Customer_Rating"].mean()

# Display KPIs with delta values (comparing to previous period)
col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}",
    f"{np.random.randint(5, 15)}%"  # Simulated growth for demo
)

col2.metric(
    "Total Profit",
    f"₹{total_profit:,.0f}",
    f"{np.random.randint(3, 12)}%"  # Simulated growth for demo
)

col3.metric(
    "Avg Profit Margin",
    f"{avg_margin:.1f}%",
    f"{np.random.randint(-2, 5)}%"  # Simulated change for demo
)

col4.metric(
    "Avg Customer Rating",
    f"{avg_rating:.2f}★",
    f"{np.random.uniform(-0.2, 0.5):.2f}"  # Simulated change for demo
)

st.markdown("---")

# Charts Section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Region")
    region_revenue = filtered_df.groupby("Region")["Revenue"].sum()
    st.bar_chart(region_revenue)

with col2:
    st.subheader("Sales by Channel")
    channel_sales = filtered_df.groupby("Channel")["Units_Sold"].sum()
    st.bar_chart(channel_sales)

# Time Series Analysis
st.subheader("Revenue Trends Over Time")
daily_revenue = filtered_df.groupby("Date")[["Revenue", "Profit"]].sum()
st.line_chart(daily_revenue)

# Product Performance
st.markdown("---")
st.subheader("Product Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    st.caption("Revenue by Product")
    product_revenue = filtered_df.groupby("Product")["Revenue"].sum().sort_values(ascending=True)
    st.bar_chart(product_revenue)

with col2:
    st.caption("Customer Ratings by Product")
    product_ratings = filtered_df.groupby("Product")["Customer_Rating"].mean().sort_values(ascending=True)
    st.bar_chart(product_ratings)

# Detailed Metrics Table
st.markdown("---")
st.subheader("Detailed Performance Metrics")

# Create summary table
summary_df = filtered_df.groupby(["Region", "Product", "Channel"]).agg({
    "Revenue": "sum",
    "Units_Sold": "sum",
    "Profit": "sum",
    "Profit_Margin": "mean",
    "Customer_Rating": "mean"
}).round(2)

st.dataframe(
    summary_df.style.highlight_max(axis=0, subset=["Revenue", "Profit"]),
    use_container_width=True
)

# Raw Data Section (Expandable)
with st.expander("View Raw Data"):
    st.dataframe(
        filtered_df.sort_values(by="Date", ascending=False),
        use_container_width=True
    )

# Footer
st.markdown("---")
st.markdown("*Dashboard created with Streamlit - Data updates daily*")

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### Dashboard Info")
st.sidebar.markdown("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
