import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Global Market Correlation", layout="wide")

st.title("📊 NIFTY vs Dow Jones vs NASDAQ - Correlation Dashboard")

# -----------------------------
# Sidebar Inputs
# -----------------------------
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2021-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

symbols = {
    "NIFTY 50": "^NSEI",
    "Dow Jones": "^DJI",
    "NASDAQ": "^IXIC"
}

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data(start, end):
    df = yf.download(list(symbols.values()), start=start, end=end)["Close"]
    df.columns = symbols.keys()
    return df

data = load_data(start_date, end_date)

# -----------------------------
# Show Raw Data
# -----------------------------
st.subheader("📌 Latest Market Data")
st.dataframe(data.tail())

# =============================
# ✅ GRAPH 1: PRICE COMPARISON
# =============================
st.subheader("📈 Graph 1: Price Comparison")

fig1, ax1 = plt.subplots()
for col in data.columns:
    ax1.plot(data.index, data[col], label=col)

ax1.set_xlabel("Date")
ax1.set_ylabel("Price")
ax1.legend()
st.pyplot(fig1)

# =============================
# ✅ GRAPH 2: NORMALIZED PRICE
# =============================
st.subheader("📉 Graph 2: Normalized Price (Base = 100)")

normalized = (data / data.iloc[0]) * 100

fig2, ax2 = plt.subplots()
for col in normalized.columns:
    ax2.plot(normalized.index, normalized[col], label=col)

ax2.set_xlabel("Date")
ax2.set_ylabel("Normalized Value")
ax2.legend()
st.pyplot(fig2)

# =============================
# ✅ GRAPH 3: DAILY RETURNS
# =============================
st.subheader("🔁 Graph 3: Daily Returns")

returns = data.pct_change().dropna()

fig3, ax3 = plt.subplots()
for col in returns.columns:
    ax3.plot(returns.index, returns[col], label=col)

ax3.set_xlabel("Date")
ax3.set_ylabel("Daily Return")
ax3.legend()
st.pyplot(fig3)

# =============================
# ✅ GRAPH 4: ROLLING CORRELATION
# =============================
st.subheader("🔗 Graph 4: 30-Day Rolling Correlation")

rolling_corr_nifty_dow = returns["NIFTY 50"].rolling(30).corr(returns["Dow Jones"])
rolling_corr_nifty_nasdaq = returns["NIFTY 50"].rolling(30).corr(returns["NASDAQ"])

fig4, ax4 = plt.subplots()
ax4.plot(rolling_corr_nifty_dow, label="NIFTY vs Dow")
ax4.plot(rolling_corr_nifty_nasdaq, label="NIFTY vs NASDAQ")

ax4.set_xlabel("Date")
ax4.set_ylabel("Rolling Correlation")
ax4.legend()
st.pyplot(fig4)

# =============================
# ✅ CORRELATION MATRIX TABLE
# =============================
st.subheader("📊 Correlation Matrix (Daily Returns)")
st.dataframe(returns.corr())

# =============================
# ✅ DOWNLOAD BUTTON
# =============================
st.subheader("⬇️ Download Data")
csv = data.to_csv().encode("utf-8")
st.download_button("Download CSV", csv, "market_data.csv", "text/csv")

st.success("✅ Dashboard Loaded Successfully")
