import streamlit as st # type: ignore
import pandas as pd # type: ignore
import plotly.express as px # type: ignore

# --- Page Configuration ---
st.set_page_config(page_title="🌿 Sri Lanka Climate Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("climate-change_lka_cleaned.csv", header=1)
    df = df.dropna()
    return df

df = load_data()

# --- Prepare Data ---
df = df.rename(columns={df.columns[0]: "Indicator"})
df_long = df.melt(id_vars=["Indicator"], var_name="Year", value_name="Value")
df_long["Year"] = pd.to_numeric(df_long["Year"], errors="coerce")
df_long["Value"] = pd.to_numeric(df_long["Value"], errors="coerce")
df_long = df_long.dropna()

# --- Sidebar Filters ---
st.sidebar.header("🔧 Filters")
indicators = sorted(df_long["Indicator"].unique())
selected_indicator = st.sidebar.selectbox("Select Indicator", indicators)
min_year = int(df_long["Year"].min())
max_year = int(df_long["Year"].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (2000, max_year))

# --- Filtered Data ---
filtered = df_long[(df_long["Indicator"] == selected_indicator) & 
                   (df_long["Year"] >= year_range[0]) & 
                   (df_long["Year"] <= year_range[1])]

# --- Header ---
st.markdown(f"## 📈 {selected_indicator}")
st.markdown(f"Showing data from **{year_range[0]}** to **{year_range[1]}**")

# --- Introduction Section with Emojis ---
st.markdown("### 🌍 Introduction")
st.markdown("""
Welcome to the **Sri Lanka Climate Change Dashboard** — a data-driven tool designed to help users explore and understand national environmental indicators from recent decades. 📊

This dashboard enables you to:
- 🔍 **Filter** climate indicators such as:
  - 🌡️ Greenhouse Gas Emissions  
  - 🌲 Forest Area  
  - ⚡ Energy Use  
  - 💧 Access to Clean Water  
  - ☀️ Renewable Energy Consumption  
- 📅 **Select a custom year range** (e.g., 2000–2024) to visualize indicator trends over time.
- 📈 **Analyze key insights** such as max values, recent levels, and averages.
- 🧾 **View raw data** for deeper analysis or validation.

This project is part of the **5DATA004W – Data Science Project Lifecycle** module and aims to promote awareness and action through clear, interactive climate data storytelling. 🌱
""")

# --- KPIs ---
latest_year = filtered["Year"].max()
latest_value = filtered[filtered["Year"] == latest_year]["Value"].values[0]
average_value = round(filtered["Value"].mean(), 2)
max_value = filtered["Value"].max()

col1, col2, col3 = st.columns(3)
col1.metric("📌 Latest Value", f"{latest_value:,.2f}")
col2.metric("📈 Max Value", f"{max_value:,.2f}")
col3.metric("📊 Average", f"{average_value:,.2f}")

# --- Layout Tabs ---
st.markdown("### 📊 Indicator Trend & Data Table")
tab1, tab2 = st.tabs(["📉 Trend Chart", "🧾 Raw Data"])

# --- Chart ---
with tab1:
    chart = px.area(filtered, x="Year", y="Value", title=f"Trend of {selected_indicator}", color_discrete_sequence=["#2ecc71"])
    chart.update_layout(xaxis_title="Year", yaxis_title="Value", plot_bgcolor="white")
    st.plotly_chart(chart, use_container_width=True)

# --- Table ---
with tab2:
    st.dataframe(filtered.reset_index(drop=True), use_container_width=True)

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
        <p style="font-size: 14px; margin-top: 20px;">
            💡 Created with ❤️ by <strong>Akshaya Sivakumar</strong><br>
            📘 <em>5DATA004W – Data Science Project Lifecycle</em><br>
            🌐 Powered by <a href="https://streamlit.io" target="_blank" style="color: #1c6e4a; text-decoration: none;">Streamlit</a> |
            📊 Visuals by <a href="https://plotly.com" target="_blank" style="color: #1c6e4a; text-decoration: none;">Plotly</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)



