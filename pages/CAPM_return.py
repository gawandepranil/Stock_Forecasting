import streamlit as st
import time
import pandas as pd
import yfinance as yf
import datetime
from pages.utils.capm_function import interactive_plot, normalize, daily_return, calculate_beta

st.set_page_config(
    page_title="CAPM",
    page_icon="📈",
    layout="wide"
)

st.title("Capital Asset Pricing Model (CAPM)")

# -------- USER INPUT --------
col1, col2 = st.columns([1, 1])

with col1:
    stocks_list = st.multiselect(
        "Choose up to 4 stocks",
        ("TSLA", "AAPL", "NFLX", "MSFT", "MGM", "AMZN", "NVDA", "GOOGL"),
        ["TSLA", "AAPL", "AMZN", "GOOGL"]
    )

with col2:
    years = st.number_input("Number of years", 1, 10, value=1)

if not stocks_list:
    st.warning("Please select at least one stock.")
    st.stop()

# -------- DATE RANGE --------
end = datetime.date.today()
start = end - datetime.timedelta(days=365 * int(years))

# -------- DOWNLOAD SP500 --------
sp500_raw = yf.download("^GSPC", start=start, end=end, progress=False)

if sp500_raw.empty:
    st.error("S&P500 (^GSPC) data not received from Yahoo. Try again later.")
    st.stop()

# Flatten MultiIndex columns produced by newer yfinance versions
if isinstance(sp500_raw.columns, pd.MultiIndex):
    sp500_raw = sp500_raw.sort_index(axis=1)
    sp500_raw.columns = [c[0] for c in sp500_raw.columns]

sp500 = sp500_raw[["Close"]].copy()
sp500.rename(columns={"Close": "sp500"}, inplace=True)
sp500 = sp500.reset_index()
sp500.rename(columns={"index": "Date"}, errors="ignore", inplace=True)
sp500["Date"] = pd.to_datetime(sp500["Date"])

# -------- DOWNLOAD STOCKS --------
stock_df = None

for stock in stocks_list:
    raw = yf.download(stock, start=start, end=end, progress=False)
    time.sleep(0.5)

    if raw.empty:
        st.warning(f"Failed to download: {stock}")
        continue

    # Flatten MultiIndex if present
    if isinstance(raw.columns, pd.MultiIndex):
        raw = raw.sort_index(axis=1)
        raw.columns = [c[0] for c in raw.columns]

    data = raw[["Close"]].copy()
    data.rename(columns={"Close": stock}, inplace=True)

    if stock_df is None:
        stock_df = data.copy()
    else:
        stock_df = stock_df.join(data, how="inner")

if stock_df is None or stock_df.empty:
    st.error("No stock data received for selected tickers. Try again later.")
    st.stop()

# Reset index safely → make sure we get a 'Date' column
stock_df = stock_df.reset_index()
stock_df.rename(columns={"index": "Date"}, errors="ignore", inplace=True)
stock_df["Date"] = pd.to_datetime(stock_df["Date"])

# -------- MERGE STOCKS + SP500 --------
stock_df = pd.merge(stock_df, sp500[["Date", "sp500"]], on="Date", how="inner")
stock_df = stock_df.reset_index(drop=True)

# -------- SHOW DATA --------
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### Dataframe head")
    st.dataframe(stock_df.head(), width='stretch')

with col2:
    st.markdown("### Dataframe tail")
    st.dataframe(stock_df.tail(), width='stretch')

# -------- PLOT --------
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### Price of all the stocks")
    st.plotly_chart(interactive_plot(stock_df), width="stretch", key="before_norm")
with col2:
    st.markdown("### Price of all the stocks (AFTER Normalizing)")
    # FIX: was passing the function object `normalize` instead of calling it
    st.plotly_chart(interactive_plot(normalize(stock_df)), width="stretch", key="after_norm")

# -------- DAILY RETURNS --------
stock_daily_return = daily_return(stock_df)

# -------- BETA & ALPHA --------
beta = {}
alpha = {}

for col in stock_daily_return.columns:
    if col not in ("Date", "sp500"):
        b, a = calculate_beta(stock_daily_return, col)
        beta[col] = b
        alpha[col] = a

# -------- BETA TABLE --------
# FIX: original code set "stock" on a non-existent column while assigning to "Stock"
beta_df = pd.DataFrame({
    "Stock":      list(beta.keys()),
    "Beta Value": [str(round(v, 2)) for v in beta.values()],
})

col1, col2 = st.columns([1, 1])   # FIX: col1/col2 had gone out of scope from the plot block
with col1:
    st.markdown("### Calculated Beta Value")
    st.dataframe(beta_df, width='stretch')

# -------- CAPM RETURN TABLE --------
rf = 0
# Annualise mean daily return of the market
market_return_annual = stock_daily_return["sp500"].mean() * 252

return_value = [
    str(round(rf + (b * (market_return_annual - rf)), 2))
    for b in beta.values()
]

return_df = pd.DataFrame({
    "Stock":        list(beta.keys()),   # FIX: was using stocks_list which can differ in order
    "Return Value": return_value,
})

with col2:
    st.markdown("### Calculated Return using CAPM")
    st.dataframe(return_df, width='stretch')