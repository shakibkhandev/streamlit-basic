import streamlit as st
import pandas as pd
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Chai Sales Dashboard",
    page_icon="☕",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 3rem !important;
    }
    .stSubheader {
        color: #34495e;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("Chai Sales Dashboard")
st.markdown("### Analyze your chai sales data with interactive visualizations 📊")

# File upload
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Data Overview Section
    st.header("1. Data Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Preview")
        st.dataframe(df)
    
    with col2:
        st.subheader("Summary Statistics")
        st.write(df.describe())
    
    # Filters Section
    st.header("2. Data Filters")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cities = sorted(df["City"].unique())
        selected_city = st.selectbox("Select City", ["All"] + list(cities))
    
    with col2:
        chai_types = sorted(df["Chai_Type"].unique())
        selected_chai = st.selectbox("Select Chai Type", ["All"] + list(chai_types))
    
    with col3:
        min_date = df["Date"].min()
        max_date = df["Date"].max()
        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
    
    # Filter the data based on selections
    filtered_df = df.copy()
    if selected_city != "All":
        filtered_df = filtered_df[filtered_df["City"] == selected_city]
    if selected_chai != "All":
        filtered_df = filtered_df[filtered_df["Chai_Type"] == selected_chai]
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= date_range[0]) &
        (filtered_df["Date"].dt.date <= date_range[1])
    ]
    
    # Analytics Section
    st.header("3. Analytics Dashboard")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = filtered_df["Revenue"].sum()
        st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    
    with col2:
        total_cups = filtered_df["Cups_Sold"].sum()
        st.metric("Total Cups Sold", f"{total_cups:,}")
    
    with col3:
        avg_revenue_per_cup = total_revenue / total_cups if total_cups > 0 else 0
        st.metric("Average Revenue per Cup", f"₹{avg_revenue_per_cup:.2f}")
    
    with col4:
        total_orders = len(filtered_df)
        st.metric("Total Orders", f"{total_orders:,}")
    
    # Visualizations
    st.header("4. Sales Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily Revenue Trend
        daily_revenue = filtered_df.groupby("Date")["Revenue"].sum()
        st.subheader("Daily Revenue Trend")
        st.line_chart(daily_revenue)
    
    with col2:
        # City-wise Revenue
        city_revenue = filtered_df.groupby("City")["Revenue"].sum()
        st.subheader("Revenue by City")
        st.bar_chart(city_revenue)
    
    # Chai Type Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Chai Type Revenue Distribution
        chai_revenue = filtered_df.groupby("Chai_Type")["Revenue"].sum()
        st.subheader("Revenue by Chai Type")
        st.bar_chart(chai_revenue)
    
    with col2:
        # Detailed Chai Performance
        chai_metrics = filtered_df.groupby("Chai_Type").agg({
            "Revenue": "sum",
            "Cups_Sold": "sum"
        }).reset_index()
        chai_metrics["Average Price"] = chai_metrics["Revenue"] / chai_metrics["Cups_Sold"]
        chai_metrics = chai_metrics.round(2)
        st.subheader("Chai Type Performance Metrics")
        st.dataframe(chai_metrics)
    
    # City and Chai Type Cross Analysis
    st.header("5. Cross Analysis")
    pivot_table = pd.pivot_table(
        filtered_df,
        values="Cups_Sold",
        index="City",
        columns="Chai_Type",
        aggfunc="sum",
        fill_value=0
    )
    st.subheader("Cups Sold by City and Chai Type")
    st.dataframe(pivot_table)
    
    # Download filtered data
    st.header("6. Export Data")
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_chai_sales.csv",
        mime="text/csv"
    )
