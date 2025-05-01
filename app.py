import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="🌿 Sri Lanka Climate Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("climate-change_lka_cleaned.csv")
    df = df.dropna()  # Drop any rows with missing values
    return df

df = load_data()

# --- Debugging: Check Data Structure ---
st.write(df.head())  # Display first few rows to ensure data structure is correct

# --- Prepare Data ---
# Ensure that the first column is for indicators and remaining columns are years
df = df.rename(columns={df.columns[0]: "Indicator"})  # Rename the first column to 'Indicator'

# Check if all columns except 'Indicator' are numeric (year columns)
year_columns = df.columns[1:]  # All columns except the 'Indicator'
df[year_columns] = df[year_columns].apply(pd.to_numeric, errors="coerce")  # Convert to numeric

# Check for any issues with the year columns
st.write(df[year_columns].head())  # Display the first few rows of year columns to debug

# Reshape the DataFrame to long format
df_long = df.melt(id_vars=["Indicator"], var_name="Year", value_name="Value")
df_long["Year"] = pd.to_numeric(df_long["Year"], errors="coerce")  # Ensure Year is numeric
df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")  # Ensure Value is numeric
df_long = df_long.dropna()  # Drop any rows with missing values

# --- Sidebar Filters ---
st.sidebar.header("🔧 Filters")
indicators = sorted(df_long["Indicator"].unique())  # List of unique indicators
selected_indicator = st.sidebar.selectbox("Select Indicator", indicators)  # Indicator selection box
min_year = int(df_long["Year"].min())  # Minimum year
max_year = int(df_long["Year"].max())  # Maximum year
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (2000, max_year))  # Year range slider

# --- Filtered Data ---
filtered = df_long[(df_long["Indicator"] == selected_indicator) & 
                   (df_long["Year"] >= year_range[0]) & 
                   (df_long["Year"] <= year_range[1])]  # Apply filters

# --- Header ---
st.markdown(f"## 📈 {selected_indicator}")
st.markdown(f"Showing data from **{year_range[0]}** to **{year_range[1]}**")

# --- Introduction Section ---
st.markdown("### 🌍 Introduction")
st.markdown("""
Welcome to the **Sri Lanka Climate Change Dashboard** — a data-driven tool that allows users to explore and understand the country's environmental indicators over time. 📊

Climate change is one of the most pressing challenges of our time, and the data available can help us make informed decisions. With this dashboard, you can:
- 🔍 **Filter** climate indicators such as:
  - 🌡️ Greenhouse Gas Emissions  
  - 🌲 Forest Area  
  - ⚡ Energy Use  
  - 💧 Access to Clean Water  
  - ☀️ Renewable Energy Consumption  
- 📅 **Choose a custom year range** (e.g., 2000–2024) to explore the trends over time.
- 📈 **Analyze insights** such as the latest values, maximum values, and averages.
- 🧾 **View the raw data** to dive deeper into the numbers and trends.

This project is part of the **5DATA004W – Data Science Project Lifecycle** module and aims to provide a better understanding of climate change in Sri Lanka and its impact on future generations. 🌱
""")

# --- KPIs ---
latest_year = filtered["Year"].max()  # Get the latest year in the filtered data
latest_value = filtered[filtered["Year"] == latest_year]["Value"].values[0]  # Get the latest value for that year
average_value = round(filtered["Value"].mean(), 2)  # Calculate the average value
max_value = filtered["Value"].max()  # Get the maximum value

col1, col2, col3 = st.columns(3)  # Create three columns for displaying metrics
col1.metric("📌 Latest Value", f"{latest_value:,.2f}")
col2.metric("📈 Max Value", f"{max_value:,.2f}")
col3.metric("📊 Average", f"{average_value:,.2f}")

# --- Layout Tabs ---
st.markdown("### 📊 Indicator Trend & Data Table")
tab1, tab2 = st.tabs(["📉 Trend Chart", "🧾 Raw Data"])

# --- Chart ---
with tab1:
    chart = px.area(filtered, x="Year", y="Value", title=f"Trend of {selected_indicator}", color_discrete_sequence=["#2ecc71"])  # Plot area chart
    chart.update_layout(xaxis_title="Year", yaxis_title="Value", plot_bgcolor="white")  # Customize chart layout
    st.plotly_chart(chart, use_container_width=True)  # Display chart

# --- Table ---
with tab2:
    st.dataframe(filtered.reset_index(drop=True), use_container_width=True)  # Display filtered data as a table

# --- Enhanced Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="
        background-color: #e8f6f3;
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    ">
        <h4 style="color: #1c6e4a;">🌿 Sri Lanka Climate Change Dashboard</h4>
        <p style="font-size: 16px; color: #333;">
            <em>"We do not inherit the Earth from our ancestors, we borrow it from our children."</em><br>
            — Native American Proverb
        </p>
        <p style="font-size: 14px; margin-top: 20px; color: #333;">
            💡 Created with ❤️ by <strong>Akshaya Sivakumar</strong><br>
            📘 <em>5DATA004W – Data Science Project Lifecycle</em><br>
            🌐 Powered by <a href="https://streamlit.io" target="_blank" style="color: #1c6e4a; text-decoration: none;">Streamlit</a> |
            📊 Visuals by <a href="https://plotly.com" target="_blank" style="color: #1c6e4a; text-decoration: none;">Plotly</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)





