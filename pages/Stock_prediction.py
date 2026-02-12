import streamlit as st
from pages.utils.model_train import get_data,get_differenceing_order,evaluate_model,get_forecast
import pandas as pd
from pages.utils.plotly_figure import plotly_table,  moving_average_forecast

st.set_page_config(
    page_title="Stock Predition",
    page_icon="chart_with_downwards_trend",
    layout="wide",
)

st.title("Stock Prediction")

col1,col2,col3=st.columns(3)

with col1:
    ticker=st.text_input("Stock TIcker","AAPL")

st.subheader("predicting next 30 days close price for:"+ticker)

close_price=get_data(ticker)
differenceing_order = get_differenceing_order(close_price)
rmse=evaluate_model(close_price,differenceing_order)

st.write("**Model RMSE score:**",rmse)
forecast=get_forecast(close_price,differenceing_order)

st.write("#### FORECAST DATA (NEXT 30 DAYS)")
fig_tail=plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail,width="stretch")


st.plotly_chart(moving_average_forecast(forecast,30),use_container_width=True    )