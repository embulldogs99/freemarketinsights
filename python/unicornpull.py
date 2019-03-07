import json
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime



def daydeltacalc(date1,date2):
    d1=datetime.strptime(date1,"%Y-%m-%d")
    d2=datetime.strptime(date2,"%Y-%m-%d")
    delta=d1-d2
    if delta.days>46 and delta.days<164:
        return 'Q'
    if delta.days<45:
        return 'M'
    if delta.days>165:
        return 'A'

def unicornpull(ticker):
    try:
        apikey='5c7a1f395c9e04.94980178'
        url='https://eodhistoricaldata.com/api/div/'+ticker+'.US?api_token='+apikey
        d=pd.read_csv(url)
        data=pd.DataFrame(d)
        entry={}
        for i in range(1,len(data.index)-1):
            entry[data['Date'].iloc[i]]={'Div':data['Dividends'].iloc[i],'Type':daydeltacalc(data['Date'].iloc[i],data['Date'].iloc[i-1])}
        return entry
    except Exception as e:
        return {}
        print(e)
