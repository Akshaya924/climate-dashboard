import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Sri Lanka Climate Dashboard", layout="centered")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("climate-change_lka_cleaned.csv")
    return df

df = load_data()

# --- Sidebar ---
st.sidebar.title("🔧 Controls")
years = df['Year'].astype(int)
year_min, year_max = int(years.min()), int(years.max())
year_range = st.sidebar.slider("Select Year Range", year_min, year_max, (1990, 2020))

indicators = df['Indicator Name'].unique()
selected_indicator = st.sidebar.selectbox("Select Indicator", sorted(indicators))

# --- Filter Data ---
filtered_df = df[(df['Indicator Name'] == selected_indicator) &
                 (df['Year'] >= year_range[0]) &
                 (df['Year'] <= year_range[1])]

# --- Title & Intro ---
st.markdown("# 🌍 Sri Lanka Climate Change Dashboard")
st.markdown("""
Welcome to the interactive dashboard exploring Sri Lanka's climate change indicators.  
Use the controls on the left to filter by year and indicator.

The dashboard visualizes key environmental trends such as:
- 📉 CO₂ emissions
- 🌳 Forest area
- ⚡ Renewable energy use
- 🌾 Agricultural land
""")
st.markdown("---")

# --- Chart ---
st.markdown(f"### 📊 {selected_indicator} ({year_range[0]} – {year_range[1]})")
fig = px.line(filtered_df, x="Year", y="Value", title=selected_indicator)
st.plotly_chart(fig, use_container_width=True)

# --- KPIs ---
st.markdown("### 📌 Key Stats")
latest_year = filtered_df['Year'].max()
latest_value = filtered_df[filtered_df['Year'] == latest_year]['Value'].values[0]
average = round(filtered_df['Value'].mean(), 2)
maximum = filtered_df['Value'].max()

col1, col2, col3 = st.columns(3)
col1.metric("Latest Value", f"{latest_value:,.2f}")
col2.metric("Max Value", f"{maximum:,.2f}")
col3.metric("Average", f"{average:,.2f}")

# --- Footer ---
st.markdown("---")
st.markdown("📘 Created by **Akshaya Sivakumar** – IIT ID: 20233116  \n🧾 Module: 5DATA004W – Data Science Project Lifecycle")


