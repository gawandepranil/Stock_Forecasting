import streamlit as st
import time
import pandas as pd
import yfinance as yf
import datetime 

st.set_page_config(
    page_title='CAPM',
    page_icon="Chart with upward trend",
    layout="wide"
)

st.title("Capital Asset Priceing Model")

# -------- USER INPUT --------
col1, col2 = st.columns([1,1])

with col1:
    stocks_list = st.multiselect(
        "Choose 4 stocks",
        ("TSLA","AAPL","NFLX","MSFT","MGM","AMZN","NVDA","GOOGL"),
        ["TSLA","AAPL","AMZN","GOOGL"]
    )

with col2:
    years = st.number_input("number of years", 1, 10)

# -------- DATE RANGE --------
end = datetime.date.today()
start = end.replace(year=end.year - years)

# -------- DOWNLOAD SP500 --------
sp500 = yf.download("^GSPC", start=start, end=end)[["Close"]]
sp500.rename(columns={"Close": "sp500"}, inplace=True)

# -------- DATE RANGE --------
end = datetime.date.today()
start = end - datetime.timedelta(days=365 * int(years))   # safer than replace()

# -------- DOWNLOAD SP500 --------
sp500 = yf.download("^GSPC", start=start, end=end, progress=False)[["Close"]]
if sp500.empty:
    st.error("S&P500 (^GSPC) data not received from Yahoo. Try again later.")
    st.stop()
sp500.rename(columns={"Close": "sp500"}, inplace=True)

# -------- DOWNLOAD STOCKS --------
stock_df = pd.DataFrame()

for stock in stocks_list:
    data = yf.download(stock, start=start, end=end, progress=False)[["Close"]] 
    time.sleep(2)

    if data.empty:
        st.warning(f"Failed to download: {stock}")
        continue

    data.rename(columns={"Close": stock}, inplace=True)

    if stock_df.empty:
        stock_df = data
    else:
        stock_df = stock_df.join(data, how="inner")

if stock_df.empty:
    st.error("No stock data received for selected tickers. Try again later.")
    st.stop()

# -------- MERGE STOCKS + SP500 --------
stock_df.reset_index(inplace=True)
sp500.reset_index(inplace=True)

stock_df = pd.merge(stock_df, sp500, on="Date", how="inner")

col1,col2=st.columns([1,1])
with col1:
    st.markdown("### Dataframe head")
    st.dataframe(stock_df.head(),use_container_width=True)
with col2:
    st.markdown("### Dataframe Tail")
    st.dataframe(stock_df.tail(), use_container_width=True)
  