📈 Stock Analysis & 5-Day Forecasting Web App

A professional Stock Analysis and Short-Term Forecasting Web Application built using:

ARIMA (Auto-optimized using Auto-ARIMA)

Streamlit

Plotly

Technical Indicators (RSI, MACD, SMA)

This app provides:

Fundamental Stock Analysis

Technical Indicator Visualization

5-Day Stock Price Forecast

RMSE Model Evaluation

🚀 Features
🔎 Stock Analysis Module

Company Overview

Market Cap, Beta, EPS, PE Ratio

Financial Ratios

Interactive Charts:

Candlestick Chart

Line Chart

Technical Indicators:

RSI (Relative Strength Index)

MACD

SMA (50-Day Moving Average)

📊 Stock Prediction Module (5-Day Forecast)

Stationarity check using ADF Test

Automatic differencing order detection

Auto ARIMA model selection

Best (p, d, q) order selection using auto_arima

5-Day future price prediction

RMSE evaluation

Moving Average visualization of forecast

🧠 Model Details
Step 1: Stationarity Check

ADF (Augmented Dickey-Fuller) test is used to determine required differencing.

Step 2: Automatic Model Selection
auto_arima(
    data,
    d=differencing_order,
    seasonal=False,
    stepwise=True,
    max_p=5,
    max_q=5
)

Step 3: ARIMA Model

Final model trained using:

ARIMA(p, d, q)

Step 4: Forecast Horizon
5 Days Ahead Forecast

Step 5: Evaluation Metric

RMSE (Root Mean Squared Error)

RMSE %

🛠 Tech Stack

Python

Streamlit

Pandas

NumPy

Statsmodels

pmdarima (Auto-ARIMA)

Scikit-learn

yFinance

Plotly

pandas-ta

📂 Project Structure
Stock_Forecasting/
│
├── pages/
│   ├── Stock_analysis.py
│   ├── Stock_prediction.py
│   └── utils/
│       ├── model_train.py
│       └── plotly_figure.py
│
├── trading_app.py
├── requirements.txt
├── app.png
└── README.md

⚙️ Installation

Clone the repository:

git clone https://github.com/gawandepranil/Stock_Forecasting.git
cd Stock_Forecasting


Install dependencies:

pip install -r requirements.txt

▶️ Run the Application
streamlit run trading_app.py

🖼 Application Preview

📌 Future Improvements

Multi-stock comparison

Hyperparameter tuning dashboard

LSTM-based deep learning forecasting

Transformer-based time series models

Cloud deployment

👨‍💻 Author

Pranil Gawande
AI & ML Enthusiast | Time Series & Forecasting