import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px 

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Banking Fraud Analytics",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Banking Transaction & Fraud Analytics Dashboard")

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
engine = create_engine("postgresql+psycopg2://admin:admin123@localhost:5433/banking_dw")

# --- Load fact table with merchant and location ---
fact = pd.read_sql("""
    SELECT f.transaction_id, f.account_id, f.merchant_id, f.amount, f.timestamp, f.fraud_flag,
           m.merchant_name, l.city AS location
    FROM fact_transactions f
    LEFT JOIN dim_merchant m ON f.merchant_id = m.merchant_id
    LEFT JOIN dim_location l ON m.location_id = l.location_id
""", engine)

# Convert timestamp to datetime
fact['timestamp'] = pd.to_datetime(fact['timestamp'])
fact['date'] = fact['timestamp'].dt.date

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("Filters")
accounts = st.sidebar.multiselect(
    "Account ID", fact['account_id'].unique(), default=fact['account_id'].unique()
)
merchants = st.sidebar.multiselect(
    "Merchant", fact['merchant_name'].unique(), default=fact['merchant_name'].unique()
)
locations = st.sidebar.multiselect(
    "Location", fact['location'].unique(), default=fact['location'].unique()
)
date_range = st.sidebar.date_input(
    "Date Range", [fact['date'].min(), fact['date'].max()]
)

# Apply filters
filtered = fact[
    fact['account_id'].isin(accounts) &
    fact['merchant_name'].isin(merchants) &
    fact['location'].isin(locations) &
    (fact['date'] >= date_range[0]) &
    (fact['date'] <= date_range[1])
]

# -------------------------------
# KPIs
# -------------------------------
st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Transactions", len(filtered))
col2.metric("Total Amount", f"${filtered['amount'].sum():,.2f}")
col3.metric("Fraud Cases", filtered['fraud_flag'].sum())

# -------------------------------
# DAILY TRANSACTION VOLUME (LINE CHART)
# -------------------------------
st.subheader("📈 Daily Transaction Volume")
daily = filtered.groupby('date')['amount'].sum().reset_index()
fig_daily = px.line(
    daily,
    x='date',
    y='amount',
    title="Daily Transaction Volume",
    markers=True,
    labels={'amount': 'Amount ($)', 'date': 'Date'},
    hover_data={'date': True, 'amount': ':.2f'}
)
fig_daily.update_traces(line=dict(color="#1f77b4", width=3), marker=dict(size=6))
fig_daily.update_layout(
    plot_bgcolor="#f9f9f9",
    paper_bgcolor="#f0f2f6",
    font=dict(color="#0f1c2c"),
)
st.plotly_chart(fig_daily, use_container_width=True)

# -------------------------------
# FRAUD RISK SCORING (TOP ACCOUNTS & MERCHANTS)
# -------------------------------
st.subheader("⚠️ Top Risky Accounts & Merchants")
top_accounts = filtered.groupby('account_id')['fraud_flag'].sum().sort_values(ascending=False).head(10)
top_merchants = filtered.groupby('merchant_name')['fraud_flag'].sum().sort_values(ascending=False).head(10)

fig_accounts = px.bar(
    top_accounts.reset_index(),
    x='account_id',
    y='fraud_flag',
    title="Top Risky Accounts",
    labels={'fraud_flag': 'Fraud Count', 'account_id': 'Account ID'},
    color='fraud_flag',
    color_continuous_scale=px.colors.sequential.Reds,
    hover_data={'fraud_flag': True, 'account_id': True}
)
fig_merchants = px.bar(
    top_merchants.reset_index(),
    x='merchant_name',
    y='fraud_flag',
    title="Top Risky Merchants",
    labels={'fraud_flag': 'Fraud Count', 'merchant_name': 'Merchant'},
    color='fraud_flag',
    color_continuous_scale=px.colors.sequential.Reds,
    hover_data={'fraud_flag': True, 'merchant_name': True}
)

col1, col2 = st.columns(2)
col1.plotly_chart(fig_accounts, use_container_width=True)
col2.plotly_chart(fig_merchants, use_container_width=True)

# -------------------------------
# DOWNLOADABLE CSV
# -------------------------------
st.subheader("💾 Download Reports")
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Filtered Transactions",
    data=csv,
    file_name='filtered_transactions.csv',
    mime='text/csv'
)

# -------------------------------
# TRANSACTION TABLE
# -------------------------------
st.subheader("📋 Transaction Details")
st.dataframe(filtered.sort_values('timestamp', ascending=False))
