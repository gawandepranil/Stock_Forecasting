import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime

import plotly.graph_objects as go

def plotly_table(dataframe):
    header_color = "#0078ff"
    row_even_color = "#f8fafd"
    row_odd_color = "#e6f0ff"

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    # first empty cell + column headers
                    values=[""] + [f"<b>{str(i)[:10]}</b>" for i in dataframe.columns],
                    line_color="white",
                    fill_color=header_color,
                    align="center",
                    font=dict(color="white", size=15),
                    height=35,
                ),
                cells=dict(
                    values=[
                        [f"<b>{str(i)}</b>" for i in dataframe.index]
                    ] + [dataframe[i] for i in dataframe.columns],
                    fill_color=[
                        [row_even_color, row_odd_color] * (len(dataframe) // 2 + 1)
                    ],
                    align="center",
                    font=dict(color="black", size=14),
                    height=30,
                ),
            )
        ]
    )
    fig.update_layout(height=400,margin=dict(l=0,r=0,t=0,b=0))
    return fig 

from dateutil.relativedelta import relativedelta
def filter_data(dataframe,num_period):
    end_date=dataframe.index[-1]
    if num_period == "1mo":
        date=end_date + relativedelta(months=-1)
    elif num_period =="5d":
        date =end_date + relativedelta(days=-5)
    elif num_period =="6mo":
        date =end_date + relativedelta(months=-6)
    elif num_period =="1y":
        date =end_date + relativedelta(years=-1)
    elif num_period =="5y":
        date =end_date + relativedelta(years=-5)
    elif num_period=="ytd":
        date=datetime.datetime(end_date.year,1,1).strftime("%y-%m-%d")
    else:
        date=dataframe.index[0]
    return dataframe.reset_index()[dataframe.reset_index()["Date"]>date]
        

def close_chart(dataframe,num_period=False):
    if num_period:
        dataframe=filter_data(dataframe,num_period)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=dataframe["Date"],y=dataframe["Open"],
                                 mode="lines",
                                 name="Open",
                                 line=dict(width=2,color="#5ab7ff")))
        fig.add_trace(go.Scatter(x=dataframe["Date"],y=dataframe["Close"],
                                 mode="lines",
                                 name="Close",
                                 line=dict(width=2,color="black")))
        fig.add_trace(go.Scatter(x=dataframe["Date"],y=dataframe["High"],
                                 mode="lines",
                                 name="High",
                                 line=dict(width=2,color="#0078ff")))
        fig.add_trace(go.Scatter(x=dataframe["Date"],y=dataframe["Low"],
                                 mode="lines",
                                 name="Low",
                                 line=dict(width=2,color="red")))
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(height=500,margin=dict(l=0,r=20,t=20,b=0),plot_bgcolor="white",paper_bgcolor="#e6f0ff",legend=dict(
            yanchor="top",
            xanchor="right"))
        return fig

def candlestick(dataframe,num_period):
    dataframe=filter_data(dataframe,num_period)
    fig=go.Figure()
    fig.add_trace(go.Candlestick(x=dataframe["Date"],
                                 open=dataframe["Open"],high=dataframe["High"],
                                 low=dataframe["Low"],close=dataframe["Close"]))
    fig.update_layout(showlegend=False,height=500,margin=dict(l=0,r=20,t=20,b=0),plot_bgcolor="White",paper_bgcolor="#e6f0ff")
    return fig

def RSI(dataframe, num_period) : 
    dataframe['RSI'] = pta.rsi(dataframe['Close']) 
    dataframe = filter_data(dataframe, num_period) 
    fig = go.Figure() 
    fig.add_trace(go.Scatter( 
        x=dataframe['Date'], 
        y=dataframe["RSI"], name = 'RSI' ,marker_color='orange', line = dict( width=2, color = 'orange'),  
        ))
    fig.add_trace(go.Scatter(  
        x=dataframe['Date'], 
        y=[70]*len(dataframe), name = 'Overbought', marker_color='red', line = dict( width=2, color = 'red', dash='dash'),  
        )) 
    fig.add_trace(go.Scatter( 
        x=dataframe['Date'], 
        y=[30]*len(dataframe),fill='tonexty', name = 'Oversold', marker_color='#79da84', line = dict( width=2, color = '#79da84', dash='dash'
        )))
    fig.update_layout(yaxis_range=[0,100], 
        height=200,plot_bgcolor = 'white', paper_bgcolor = '#e6f0ff',margin=dict(l=0, r=0, t=0, b=0), legend=dict(orientation="h", 
    yanchor="top", 
    y=1.02, 
    xanchor="right",
    x=1
        ))
    return fig

def Moving_average_stock(dataframe,num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'],50) 
    dataframe = filter_data(dataframe,num_period) 
    fig = go.Figure()  
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'], mode='lines', name='Open', line = dict( width=2, color = '#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'], mode='lines', name='Close', line = dict( width=2,color = 'black') ))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'], mode='lines', name='High', line = dict( width=2, color = '#0078ff'))) 
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'], mode='lines', name='Low', line = dict( width=2, color = 'red') ) ) 
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'], mode='lines',name='SMA 50', line = dict( width=2, color = 'purple')))  
    fig.update_xaxes(rangeslider_visible=True) 
    fig.update_layout(height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor = 'white',paper_bgcolor = '#e6f0ff', legend=dict( 
    yanchor="top", 
    xanchor="right"
    ))
    return fig
def moving_average_forecast(df, window):

    df = df.copy()
    df = df.reset_index()   # VERY IMPORTANT

    # Now index becomes a column
    date_col = df.columns[0]   # first column will be Date
    value_col = 'Close'

    df['SMA'] = df[value_col].rolling(window).mean()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df[date_col],
        y=df[value_col],
        mode='lines',
        name='Forecast'
    ))

    fig.add_trace(go.Scatter(
        x=df[date_col],
        y=df['SMA'],
        mode='lines',
        name=f'SMA {window}'
    ))

    return fig

def MACD(dataframe, num_period): 
    macd = pta.macd(dataframe['Close']).iloc[:,0] 
    macd_signal = pta.macd(dataframe['Close']).iloc[:,1] 
    macd_hist = pta.macd(dataframe['Close']).iloc[:,2] 
    dataframe['MACD'] = macd 
    dataframe['MACD Signal']=macd_signal
    dataframe['MACD Hist'] = macd_hist 
    dataframe = filter_data(dataframe,num_period) 
    fig = go.Figure() 
    fig.add_trace(go.Scatter( 
        x=dataframe['Date'], 
        y=dataframe['MACD'], 
        name = 'MACD',
        marker_color='orange', 
        line = dict( width=2, color = 'orange'),  
            ))
    fig.add_trace(go.Scatter(  
        x=dataframe['Date'], 
        y=dataframe['MACD Signal'], 
        name = 'Overbought', 
        marker_color='red', 
        line = dict( width=2, color = 'red', dash='dash'),
        ))
    fig.update_layout( 
        height=200,
        plot_bgcolor = 'white', 
        paper_bgcolor = '#e1efff',
        margin=dict(l=0, r=0, t=0, b=0), 
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=1 
            )
        )
    return fig 