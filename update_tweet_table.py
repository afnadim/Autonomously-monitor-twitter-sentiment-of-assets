import time
import datetime
import plotly.graph_objs as go
import sqlite3
import pandas as pd

colors = {
    'background': ' #050505',
    'light blue': '#7FDBFF',
    'red': '#FF0000',
    'aqua': '#00FFFF',
    'green': '#008000',
    'blue': '#0000FF',
    'white':'#edf4f4',
    'deep blue':'#4333ff'
}

def update_table(select_financial_asset):
    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
    df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 5", conn ,params=('%' + select_financial_asset + '%',))
    #df.sort_values('unix', inplace=True)
    #taking in the sentiment value of the tweet in a list so we can use it later to change the
    #row color accordinly with the value
    vals=[]
    for i in range(5):
        vals.append(df.sentiment.values[i])
    trace = go.Table(
        columnwidth=[0.2, 0.7, 0.2],
        header=dict(
            #values=list(df.columns[1:]),
            values=['Time', 'Tweets', 'Sentiment'],
            font=dict(size=12),
            line = dict(color='#0000FF'),
            align = 'left',
            fill = dict(color=' #7fb3d5'),
        ),

        cells=dict(
            values=[df[k].tolist() for k in df.columns[0:]],
            line = dict(color='#0000FF'),
            font=dict(size=12),
            align = 'left',
            fill = dict(
            #clours accordingly with the sentiment valu of the Tweets
            color=[[
            '#abebc6' if val>0 else
            '#f1948a' if val<0
            else '#eaeded'
            for val in vals
            ] ])))
    data = [trace]
    layout=go.Layout(
    width=450,
    #width=695,
    height=300,
    autosize=False,
    margin=go.layout.Margin(
        l=30,
        r=30,
        b=30,
        t=70,
        pad=5
    ),
    font=dict(family='Courier New, monospace', size=11, color='blue'),
    title='Live Tweets related to :'+select_financial_asset)
    fig= go.Figure(data=data,layout=layout)
    return fig
