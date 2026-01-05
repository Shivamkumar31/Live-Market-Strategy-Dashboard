import streamlit as st
import yfinance as yf
import numpy as np

st.title("Live Market Strategy Dashboard")

symbol = st.selectbox("Select Stock", ["RELIANCE.NS", "TCS.NS", "INFY.NS"])

data = yf.download(symbol, period="1y")
data['returns'] = data['Close'].pct_change()

data['SMA20'] = data['Close'].rolling(20).mean()
data['SMA50'] = data['Close'].rolling(50).mean()

data['signal'] = np.where(data['SMA20'] > data['SMA50'], 1, 0)
data['strategy_returns'] = data['signal'].shift(1) * data['returns']
cumulative_pnl = (1 + data['strategy_returns']).cumprod()

st.metric("Sharpe Ratio", round(
    data['strategy_returns'].mean() / data['strategy_returns'].std() * np.sqrt(252), 2))

st.line_chart(cumulative_pnl)
