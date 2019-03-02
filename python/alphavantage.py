
import requests
import bs4
from bs4 import BeautifulSoup
import warnings
import time
import datetime
import json
import pandas as pd
import io
import re
import psycopg2
import quandl
import random
from datetime import date, timedelta

warnings.filterwarnings('ignore')
today=datetime.date.today()
searchtoday=today.strftime('%Y-%m-%d')
yesterday=datetime.date.today()-timedelta(1)
searchyesterday=yesterday.strftime('%Y-%m-%d')
twodayago=datetime.date.today()-timedelta(2)
searchtwodayago=twodayago.strftime('%Y-%m-%d')
threedayago=datetime.date.today()-timedelta(3)
searchthreedayago=threedayago.strftime('%Y-%m-%d')

apikey='DFL9CKR6I3AXY7CC'

def alphavantagepricepull(ticker):
    try:
        url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ticker+"&apikey="+apikey
        data=requests.get(url)
        binary=data.content
        output=json.loads(binary)
        price=output['Time Series (Daily)'][searchtoday]['5. adjusted close']
        return price
    except:
        try:
            url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ticker+"&apikey="+apikey
            data=requests.get(url)
            binary=data.content
            output=json.loads(binary)
            price=output['Time Series (Daily)'][searchyesterday]['5. adjusted close']
            return price
        except:
            try:
                url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ticker+"&apikey="+apikey
                data=requests.get(url)
                binary=data.content
                output=json.loads(binary)
                price=output['Time Series (Daily)'][searchtwodayago]['5. adjusted close']
                return price
            except:
                try:
                    url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ticker+"&apikey="+apikey
                    data=requests.get(url)
                    binary=data.content
                    output=json.loads(binary)
                    price=output['Time Series (Daily)'][searchthreedayago]['5. adjusted close']
                    return price
                except:
                    return 0.00000001
