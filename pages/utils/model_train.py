import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error,r2_score
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np 
from datetime import datetime,timedelta
from sklearn.preprocessing import StandardScaler

def get_data(ticker):
    stock_data=yf.download(ticker,start="2024-01-01")
    close = stock_data["Close"]
    close.index = pd.to_datetime(close.index)
    close = close.sort_index()
    close = close.asfreq("B").ffill()
    close.index.name = "Date"

    return close
def stationary_check(close_price):
    adf_test=adfuller(close_price)
    p_value=round(adf_test[1],3)
    return p_value

def get_rolling_mean(close_price):
    rolling_price=close_price.rolling(window=7).mean().dropna()
    return rolling_price

def get_differenceing_order(close_price):
    p_value = stationary_check(close_price)
    d = 0
    
    while p_value > 0.05 and d<3 :
        d += 1
        close_price = close_price.diff().dropna()
        p_value = stationary_check(close_price)
    
    return d
    
def fit_model(data, differencing_order):

    model = ARIMA(data, order=(2, differencing_order, 2))
    model_fit = model.fit()

    forecast = model_fit.get_forecast(steps=30)
    predictions = forecast.predicted_mean
    return predictions

def evaluate_model(original_price,differencing_order):
    train_data,test_data=original_price[:-30],original_price[-30:]
    predictions=fit_model(train_data,differencing_order)
    predictions = predictions.reindex(test_data.index)
    rmse=np.sqrt(mean_squared_error(test_data.dropna(),predictions.dropna()))
    return round(rmse,2)

def get_forecast(original_price, differencing_order):
    predictions = fit_model(original_price, differencing_order)
    forecast_df = predictions.to_frame(name="Close")
    forecast_df.index.name = "Date"
    return forecast_df