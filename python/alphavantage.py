
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
import numpy as np


warnings.filterwarnings('ignore')

apikey='DFL9CKR6I3AXY7CC'

def alphavantagepricepull(ticker):
    try:
        url="https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol="+ticker+"&apikey="+apikey
        data=requests.get(url)
        binary=data.content
        output=json.loads(binary)
        price=output['Global Quote']['05. price']
        return price
    except:
        return 0.00000001

def alphavantageyearbenchmark():
    url='https://www.alphavantage.co/query?function=SECTOR&apikey=DFL9CKR6I3AXY7CC'
    data=requests.get(url)
    jsondata=json.loads(data.content)
    performancedata=jsondata["Rank G: 1 Year Performance"]
    array=[]
    for d in performancedata:
        if performancedata[d]!=None:
            array.append(float(performancedata[d].replace('%','')))
    return round(np.mean(array),2)
