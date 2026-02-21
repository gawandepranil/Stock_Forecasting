import streamlit as st
import sys
import os

# Fix import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.model_train import get_data, get_differenceing_order, evaluate_model, get_forecast
from utils.plotly_figure import plotly_table, moving_average_forecast
import pandas as pd

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="📈",
    layout="wide",
)

st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input("Stock Ticker", "AAPL")

st.subheader("Predicting next 5 days close price for: " + ticker)

close_price = get_data(ticker)
differenceing_order = get_differenceing_order(close_price)
rmse = evaluate_model(close_price, differenceing_order, test_days=5)

st.write("**Model RMSE score:**", rmse)
forecast = get_forecast(close_price, differenceing_order)

st.write("#### FORECAST DATA (NEXT 5 DAYS)")
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, key="forecast_table")

st.plotly_chart(moving_average_forecast(forecast, 30), key="forecast_chart")