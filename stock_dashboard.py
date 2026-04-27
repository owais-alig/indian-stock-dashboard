import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="Indian Stock Market Dashboard", layout="wide")
st.title("Indian Stock Market Dashboard (2020-2024)")

conn = sqlite3.connect('stock_market.db')
df = pd.read_sql("SELECT * FROM stock_prices ORDER BY Date ASC", conn)
conn.close()

df = df.set_index('Date')
df.index = pd.to_datetime(df.index)

tickers = df.columns.tolist()

# ---- Sidebar ----
st.sidebar.header("Filters")
selected_stock = st.sidebar.selectbox("Select Stock", tickers)

# ---- Row 1: Metrics ----
first_price = df[selected_stock].iloc[0]
last_price = df[selected_stock].iloc[-1]
returns_pct = round(float((last_price - first_price) / first_price * 100), 2)
daily_ret = df[selected_stock].pct_change().dropna()
volatility = round(daily_ret.std() * (252 ** 0.5) * 100, 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Start Price (Jan 2020)", f"₹{first_price:.2f}")
col2.metric("End Price (Dec 2024)", f"₹{last_price:.2f}")
col3.metric("5-Year Return", f"{returns_pct}%")
col4.metric("Annual Volatility", f"{volatility}%")

# ---- Row 2: Price + Moving Averages ----
st.subheader(f"{selected_stock} — Price & Moving Averages")
ma_df = pd.DataFrame()
ma_df['Price'] = df[selected_stock]
ma_df['MA50'] = df[selected_stock].rolling(50).mean()
ma_df['MA200'] = df[selected_stock].rolling(200).mean()

fig1, ax1 = plt.subplots(figsize=(14, 4))
ax1.plot(ma_df.index, ma_df['Price'], label='Price', linewidth=1, color='steelblue')
ax1.plot(ma_df.index, ma_df['MA50'], label='50-Day MA', linewidth=1.5, color='orange')
ax1.plot(ma_df.index, ma_df['MA200'], label='200-Day MA', linewidth=1.5, color='red')
ax1.legend()
ax1.set_ylabel("Price (INR)")
st.pyplot(fig1)

# ---- Row 3: Returns Bar + Risk vs Return ----
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("5-Year Returns — All Stocks")
    all_returns = ((df.iloc[-1] - df.iloc[0]) / df.iloc[0] * 100).round(2).sort_values(ascending=True)
    colors = ['green' if x > 100 else 'steelblue' if x > 50 else 'salmon' for x in all_returns.values]
    fig2, ax2 = plt.subplots(figsize=(7, 6))
    ax2.barh(all_returns.index, all_returns.values, color=colors)
    ax2.set_xlabel("Return (%)")
    st.pyplot(fig2)

with col_b:
    st.subheader("Risk vs Return")
    all_vol = (df.pct_change().dropna().std() * (252 ** 0.5) * 100).round(2)
    fig3, ax3 = plt.subplots(figsize=(7, 6))
    ax3.scatter(all_vol, all_returns, s=80, color='steelblue')
    for ticker in all_returns.index:
        ax3.annotate(ticker.replace('.NS', ''), (all_vol[ticker], all_returns[ticker]),
                     textcoords='offset points', xytext=(5, 3), fontsize=7)
    ax3.set_xlabel("Volatility (%)")
    ax3.set_ylabel("Return (%)")
    st.pyplot(fig3)
