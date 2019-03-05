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
    if delta.days>80 and delta.days<120:
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
        entry['Div']=data['Dividends'].iloc[-2]
        entry['DivDate']=data['Date'].iloc[-2]
        entry['DivType']=daydeltacalc(data['Date'].iloc[-2],data['Date'].iloc[-3])
        entry['T1Div']=data['Dividends'].iloc[-3]
        entry['T1DivDate']=data['Date'].iloc[-3]
        entry['T1DivType']=daydeltacalc(data['Date'].iloc[-3],data['Date'].iloc[-4])
        entry['T2Div']=data['Dividends'].iloc[-4]
        entry['T2DivDate']=data['Date'].iloc[-4]
        entry['T2DivType']=daydeltacalc(data['Date'].iloc[-4],data['Date'].iloc[-5])
        entry['T3Div']=data['Dividends'].iloc[-5]
        entry['T3DivDate']=data['Date'].iloc[-5]
        entry['T3DivType']=daydeltacalc(data['Date'].iloc[-5],data['Date'].iloc[-6])
        entry['T4Div']=data['Dividends'].iloc[-6]
        entry['T4DivDate']=data['Date'].iloc[-6]
        entry['T4DivType']=daydeltacalc(data['Date'].iloc[-6],data['Date'].iloc[-7])
        entry['T5Div']=data['Dividends'].iloc[-7]
        entry['T5DivDate']=data['Date'].iloc[-7]
        entry['T5DivType']=daydeltacalc(data['Date'].iloc[-7],data['Date'].iloc[-8])
        return entry
    except Exception as e:
        return {}
        print(e)
