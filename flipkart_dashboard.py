import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Load Data using full path
df = pd.read_csv(r"C:\Users\richy\Documents\Spring 2025\BSAN 406\BSAN 406 Term Project\Flipkart Mobile - 2.csv")

# Data Cleaning
df['ROM'] = df['ROM'].astype(str).str.extract(r'(\d+)').astype(float)
df['RAM'] = df['RAM'].astype(str).str.extract(r'(\d+)').astype(float)
df['battery_capacity'] = df['battery_capacity'].astype(str).str.extract(r'(\d+)').astype(float)
df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')
df['sales_price'] = pd.to_numeric(df['sales_price'], errors='coerce')
df['discount_percent'] = pd.to_numeric(df['discount_percent'], errors='coerce')
df['sales'] = pd.to_numeric(df['sales'], errors='coerce')
df = df.dropna(subset=['ROM', 'RAM', 'battery_capacity', 'ratings', 'sales_price', 'discount_percent', 'sales'])

# Streamlit Layout
st.set_page_config(layout="wide")
st.title("Flipkart Smartphone Insights Dashboard")

# Section 1: Spec-Driven Consumer Behavior
st.header("1. Spec-Driven Consumer Behavior")
col1, col2 = st.columns(2)
with col1:
    spec = st.selectbox("Select Specification to Explore:", ["ROM", "RAM", "battery_capacity"])
with col2:
    st.write("Ratings distribution by selected specification")
fig1, ax1 = plt.subplots()
sns.boxplot(x=df[spec], y=df['ratings'], ax=ax1)
ax1.set_title(f"Customer Ratings by {spec}")
ax1.set_xlabel(f"{spec} (Standardized Units)")
ax1.set_ylabel("Customer Ratings")
plt.xticks(rotation=45)
st.pyplot(fig1)

# Section 2: Price Sensitivity & Discount Impact
st.header("2. Price Sensitivity & Discount Impact")
col3, col4 = st.columns(2)
with col3:
    min_price, max_price = int(df['sales_price'].min()), int(df['sales_price'].max())
    price_range = st.slider("Select Price Range (₹):", min_price, max_price, (10000, 30000))
    df_filtered = df[(df['sales_price'] >= price_range[0]) & (df['sales_price'] <= price_range[1])]
    fig2 = px.scatter(
        df_filtered, x="sales_price", y="sales",
        size="discount_percent", color="discount_percent",
        color_continuous_scale="Turbo",
        title="Sales Volume by Price and Discount",
        labels={"sales_price": "Sales Price (₹)", "sales": "Units Sold", "discount_percent": "Discount %"}
    )
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    discount_bins = pd.cut(df_filtered['discount_percent'], bins=[0, 0.05, 0.10, 0.20, 0.30, 1.00],
                           labels=['0–5%', '6–10%', '11–20%', '21–30%', '>30%'])
    df_filtered['discount_bin'] = discount_bins
    bar_df = df_filtered.groupby("discount_bin")["sales"].mean().reset_index()
    fig3 = px.bar(bar_df, x="discount_bin", y="sales", color="discount_bin",
                  title="Average Sales by Discount Range",
                  labels={"discount_bin": "Discount Bracket", "sales": "Avg Units Sold"},
                  color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig3, use_container_width=True)

# Section 3: Explore Model Performance
st.header("3. Explore Model Performance")
col5, col6 = st.columns(2)
with col5:
    selected_ram = st.slider("Filter Models by RAM (GB):", min_value=1, max_value=12, value=4)
    filtered_df = df[df['RAM'] == selected_ram]
with col6:
    st.write("Hover for discount and battery info")
fig4 = px.scatter(
    filtered_df, x="sales_price", y="ratings",
    size="sales", color="ROM",
    hover_data=["battery_capacity", "discount_percent"],
    title=f"Sales vs Ratings for Models with {selected_ram} GB RAM",
    labels={"sales_price": "Price (₹)", "ratings": "Customer Ratings", "ROM": "Storage (GB)"},
    color_continuous_scale="Plasma"
)
st.plotly_chart(fig4, use_container_width=True)
