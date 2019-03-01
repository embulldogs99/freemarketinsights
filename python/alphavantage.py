
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

warnings.filterwarnings('ignore')
today=datetime.date.today()
searchdate=today.strftime('%Y-%m-%d')

apikey='DFL9CKR6I3AXY7CC'

def alphavantagepricepull(ticker):
    try:
        url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol="+ticker+"&apikey="+apikey
        data=requests.get(url)
        binary=data.content
        output=json.loads(binary)
        price=output['Time Series (Daily)'][searchdate]['5. adjusted close']
        return price
    except:
        return None
