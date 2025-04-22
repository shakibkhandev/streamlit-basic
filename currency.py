import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Set page config
st.set_page_config(page_title="Advanced Currency Converter", layout="wide")

# Custom CSS to improve appearance
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stSelectbox, .stNumberInput {
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🌍 Advanced Currency Converter")
st.markdown("Convert currencies, view historical rates, and compare multiple currencies in real-time.")

# Main conversion section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Currency Converter")
    amount = st.number_input("Enter Amount", min_value=0.01, value=1.0, step=0.01)
    
    # List of common currencies
    currencies = [
        "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "INR", 
        "NZD", "SGD", "HKD", "SEK", "KRW", "MXN"
    ]
    
    source_currency = st.selectbox("From Currency:", currencies, index=currencies.index("USD"))
    target_currency = st.selectbox("To Currency:", currencies, index=currencies.index("EUR"))

    if st.button("Convert", key="convert_button"):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{source_currency}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                rate = data["rates"][target_currency]
                converted = rate * amount
                
                # Display result in a nice format
                st.markdown(f"""
                    <div style='padding: 1rem; background-color: #e6f3ff; border-radius: 5px;'>
                        <h3>{amount:,.2f} {source_currency} = {converted:,.2f} {target_currency}</h3>
                        <p>Exchange Rate: 1 {source_currency} = {rate:,.4f} {target_currency}</p>
                        <p>Last Updated: {data['date']}</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Failed to fetch conversion rate")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

with col2:
    st.subheader("Multi-Currency Comparison")
    base = st.selectbox("Select Base Currency:", currencies, key="comparison_base")
    
    if st.button("Compare", key="compare_button"):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{base}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                rates = data["rates"]
                
                # Create comparison table
                comparison_data = []
                for curr in currencies:
                    if curr != base:
                        comparison_data.append({
                            "Currency": curr,
                            f"1 {base} =": f"{rates[curr]:.4f} {curr}",
                            f"1 {curr} =": f"{(1/rates[curr]):.4f} {base}"
                        })
                
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True)
            else:
                st.error("Failed to fetch comparison data")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Historical Rates Chart
st.subheader("Historical Exchange Rates (Last 7 Days)")
chart_source = st.selectbox("Select Base Currency:", currencies, key="chart_base")
chart_target = st.selectbox("Select Target Currency:", currencies, key="chart_target")

if st.button("Show Historical Rates", key="history_button"):
    try:
        # Get current date
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Collect historical data
        historical_rates = []
        dates = []
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            url = f"https://api.exchangerate-api.com/v4/latest/{chart_source}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                rate = data["rates"][chart_target]
                historical_rates.append(rate)
                dates.append(date_str)
            
            current_date += timedelta(days=1)
        
        # Create and display chart using Streamlit's native line chart
        df = pd.DataFrame({
            "Date": dates,
            "Exchange Rate": historical_rates
        })
        df = df.set_index("Date")
        
        st.line_chart(df)
        
        # Display the data in a table below the chart
        st.write("Historical Data:")
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"An error occurred while fetching historical data: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Data provided by ExchangeRate-API")
