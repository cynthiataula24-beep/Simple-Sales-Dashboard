import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Interactive Sales Dashboard")

# -----------------------
# CREATE DATA
# -----------------------
np.random.seed(42)

df = pd.DataFrame({
    "date": pd.date_range(start="2023-01-01", periods=200),
    "sales": np.random.randint(1000, 5000, 200),
    "category": np.random.choice(["Electronics", "Clothing", "Food"], 200),
    "region": np.random.choice(["Nairobi", "Mombasa", "Kisumu"], 200)
})

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("Filters")

# Date filter
start_date = st.sidebar.date_input("Start Date", df["date"].min())
end_date = st.sidebar.date_input("End Date", df["date"].max())

# Category filter
category = st.sidebar.multiselect(
    "Select Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

# Region filter
region = st.sidebar.multiselect(
    "Select Region",
    options=df["region"].unique(),
    default=df["region"].unique()
)

# -----------------------
# FILTER DATA
# -----------------------
filtered_df = df[
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date)) &
    (df["category"].isin(category)) &
    (df["region"].isin(region))
]

# -----------------------
# METRICS
# -----------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{filtered_df['sales'].sum():,}")
col2.metric("Average Sales", f"{filtered_df['sales'].mean():.0f}")
col3.metric("Transactions", len(filtered_df))

# -----------------------
# CHARTS
# -----------------------

# 1. Line Chart
fig1 = px.line(
    filtered_df,
    x="date",
    y="sales",
    color="category",
    title="Sales Over Time"
)

# 2. Bar Chart
fig2 = px.bar(
    filtered_df,
    x="category",
    y="sales",
    color="category",
    title="Sales by Category"
)

# 3. Histogram
fig3 = px.histogram(
    filtered_df,
    x="sales",
    nbins=20,
    title="Sales Distribution"
)

# 4. Boxplot
fig4 = px.box(
    filtered_df,
    x="region",
    y="sales",
    color="region",
    title="Sales by Region"
)

# -----------------------
# LAYOUT
# -----------------------
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)
    st.plotly_chart(fig4, use_container_width=True)