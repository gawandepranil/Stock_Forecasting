import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import ta
from pages.utils.plotly_figure import plotly_table
import datetime
from pages.utils.plotly_figure import (
    plotly_table,
    close_chart,
    candlestick,
    RSI,
    MACD,
    Moving_average_stock
)


#setting page congif
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="page_with_curl",
    layout="wide",
)

st.title("Stock Anaysis")

col1,col2,col3=st.columns(3)
today=datetime.date.today()

with col1:
    ticker=st.text_input("Stock Ticker","TSLA")
with col2:
    start_date=st.date_input("Choose Start Data",datetime.date(today.year -1,today.month,today.day))
with col3:
    end_date=st.date_input("Choose End Data",datetime.date(today.year,today.month,today.day))
st.subheader(ticker)
stock=yf.Ticker(ticker)
st.write(f"**LongBusinessSummy:** {stock.info.get('longBusinessSummary','Not available')}")
st.write(f"**Sector:** {stock.info.get('secto','Not available')}")
st.write(f"**Full Time Employees:** {stock.info.get('fullTimeEmployees','Not available')}")
st.write(f"**Website:**{stock.info.get('website','Not available')}")



col1,col2=st.columns(2) 
with col1:
    df=pd.DataFrame(index=["Marke Cap","Beta","EPS","PE Ratio"])
    df[" "]=[
        stock.info["marketCap"],
        stock.info["beta"],
        stock.info["trailingEps"],
        stock.info["trailingPE"]
        ]
    fig_df=plotly_table(df)
    st.plotly_chart(fig_df,use_container_width=True)

with col2: 
    df = pd. DataFrame(index = ['Qucik Ratio', 'Revenue per share','Profit Margins', 'Debt to Equity', 'Return on Equity']) 
    df[""] = [stock.info["quickRatio"],stock.info["revenuePerShare"],stock.info["profitMargins"], stock.info["debtToEquity"],stock.info["returnOnEquity"]]
    fig_df = plotly_table(df) 
    st.plotly_chart(fig_df, use_container_width=True) 


data=yf.download(ticker,start=start_date,end=end_date)
data.columns = data.columns.droplevel(1)

col1,col2,col3=st.columns(3)
daily_change=data["Close"].iloc[-1]-data["Close"].iloc[-2]
col1.metric("Daily chnage",str(round(data["Close"].iloc[-1],2)),str(round(daily_change,2)))


last_10_df=data.tail(10).sort_index(ascending=False).round(3)
fig_df = plotly_table(last_10_df) 
st.write("#### Historical Data (Last 10 days)")
st.plotly_chart(fig_df, use_container_width=True) 

if "num_period" not in st.session_state:
    st.session_state.num_period = "1y"

col1,col2,col3,col4,col5,col6,col7 = st.columns(7)

with col1:
    if st.button("5D"):
        st.session_state.num_period = "5d"

with col2:
    if st.button("1M"):
        st.session_state.num_period = "1mo"

with col3:
    if st.button("6M"):
        st.session_state.num_period = "6mo"

with col4:
    if st.button("YTD"):
        st.session_state.num_period = "ytd"

with col5:
    if st.button("1Y"):
        st.session_state.num_period = "1y"

with col6:
    if st.button("5Y"):
        st.session_state.num_period = "5y"

with col7:
    if st.button("MAX"):
        st.session_state.num_period = "max"

num_period = st.session_state.num_period
st.write("Selected period:", num_period)


col1,col2,col3=st.columns([1,1,4])
with col1:
    chart_type=st.selectbox("",("Candle","Line"))
with col2:
    if chart_type=="Candle":
        indicators=st.selectbox("",("RSI","MACD"))
    else:
        indicators=st.selectbox("",("RSI","MOVING AVERAGE","MACD"))
ticker_=yf.Ticker(ticker)
new_df1=ticker_.history(period="max")
data1=ticker_.history(period="max")
if num_period=="":
    if chart_type=="Candle" and indicators =="RSI":
        st.plotly_chart(candlestick(data1,"1y"),use_container_width=True)
        st.plotly_chart(RSI(data1,"1y"),use_container_width=True)

    if chart_type=="Candle" and indicators =="MACD":
        st.plotly_chart(candlestick(data1,"1y"),use_container_width=True)
        st.plotly_chart(MACD(data1,"1y"),use_container_width=True)
        
    if chart_type=="Line" and indicators =="RSI":
        st.plotly_chart(close_chart(data1,"1y"),use_container_width=True)
        st.plotly_chart(RSI(data1,"1y"),use_container_width=True)

    if chart_type=="Line" and indicators =="MOVING AVERAGE":
        st.plotly_chart(Moving_average_stock(data1,"1y"),use_container_width=True)

    if chart_type=="Line" and indicators =="MACD":
        st.plotly_chart(close_chart(data1,"1y"),use_container_width=True)
        st.plotly_chart(MACD(data1,"1y"),use_container_width=True)



else:
    if chart_type=="Candle" and indicators == "RSI":
        st.plotly_chart(candlestick(new_df1,num_period),use_container_width=True)
        st.plotly_chart(RSI(new_df1,num_period),use_container_width=True)

    if chart_type=="Candle" and indicators == "MACD":
        st.plotly_chart(candlestick(new_df1,num_period),use_container_width=True)
        st.plotly_chart(MACD(new_df1,num_period),use_container_width=True)
    
    if chart_type=="Line" and indicators == "RSI":
        st.plotly_chart(close_chart(new_df1,num_period),use_container_width=True)
        st.plotly_chart(RSI(new_df1,num_period),use_container_width=True)

    if chart_type=="Line" and indicators == "MACD":
        st.plotly_chart(close_chart(new_df1,num_period),use_container_width=True)
        st.plotly_chart(MACD(new_df1,num_period),use_container_width=True)

    if chart_type=="Line" and indicators == "MOVING AVERAGE":
        st.plotly_chart(Moving_average_stock(new_df1,num_period),use_container_width=True)
        
