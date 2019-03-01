
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


def nasdaqpull(ticker):
    url="https://www.nasdaq.com/symbol/"+ticker
    with requests.Session() as c:
        x=c.get(url)
        soup=BeautifulSoup(x.content, "html.parser")
        summary=soup.find_all("div",{"class":"table-cell"})

        i=-2
        yrtrgttrig=i+1
        pricehighlowtrig=i+1
        voltrig=i+1
        avgvoltrig=i+1
        pricetrig=i+1
        highlowtrig=i+1
        captrig=i+1
        petrig=i+1
        forpetrig=i+1
        epstrig=i+1
        divtrig=i+1
        exdivtrig=i+1
        divpaytrig=i+1
        divyieldtrig=i+1
        betatrig=i+1

        x=1
        i=0
        data={}
        while i<40:
            for z in summary:
                z=z.text
                z=str(z)
                z=z.replace('\\','').replace('\\r','').replace('\\n','').replace('\xa0','').replace('$','').replace('%','').replace('\r\n','').replace(' ','').replace(',','').strip()

                if z.find('1YearTarget')>=0:
                    yrtrgttrig=i+1
                if z.find("Today'sHigh/Low")>=0:
                    pricehighlowtrig=i+x
                if z.find('ShareVolume')>=0:
                    voltrig=i+x
                if z.find('50DayAvg')>=0:
                    avgvoltrig=i+x
                if z.find('PreviousClose')>=0:
                    pricetrig=i+x
                if z.find('52Week')>=0:
                    highlowtrig=i+x
                if z.find('MarketCap')>=0:
                    captrig=i+x
                if z.find('P/ERatio')>=0:
                    petrig=i+x
                if z.find('ForwardP/E')>=0:
                    forpetrig=i+x
                if z.find('EPS')>=0:
                    epstrig=i+x
                if z.find('AnnualizedDividend')>=0:
                    divtrig=i+x
                if z.find('ExDividendDate')>=0:
                    exdivtrig=i+x
                if z.find('DividendPaymentDate')>=0:
                    divpaytrig=i+x
                if z.find('CurrentYield')>=0:
                    divyieldtrig=i+x
                if z.find('Beta')>=0:
                    betatrig=i+x
                i+=1

        i=0
        while i<40:
            for q in summary:

                q=q.text
                q=str(q)
                q=q.replace('\\','').replace('\\r','').replace('\\n','').replace('\xa0','').replace('$','').replace('%','').replace('\r\n','').replace(',','')

                data['Ticker']=ticker
                if i==pricetrig:
                    data['Price']=float(q)
                if i==yrtrgttrig:
                    try:
                        data['Target']=float(q)
                    except:
                        data['Target']=''
                if i==voltrig:
                  data['Volume']=float(q)
                if i==avgvoltrig:
                    data['50VolumeAvg']=float(q)
                if i==highlowtrig:
                    mid=q.find('/')
                    high=q[:mid]
                    low=q[mid+1:]
                    data['52wkHigh']=float(high)
                    data['52wkLow']=float(low)
                if i==captrig:
                    data['MarketCap']=float(q)
                if i==petrig:
                    data['P/E']=float(q)
                if i==forpetrig:
                    try:
                        data['1yr_P/E']=float(q)
                    except:
                        data['1yr_P/E']=''
                if i==epstrig:
                    data['EPS']=float(q)
                if i==divtrig:
                    try:
                        data['Anul_Div']=float(q)
                    except:
                        data['Anul_Div']='-'
                months=['J','F','M','A','S','O','N','D']
                if i==exdivtrig:
                    for m in months:
                        if q.find(m)>=0:
                            start=q.find(m)
                            striplength=len(q.strip().replace(' ',''))
                            data['Ex_Div_Date']=q[start:start+striplength+2].replace('.','')
                if i==divpaytrig:
                    for m in months:
                        if q.find(m)>=0:
                            start=q.find(m)
                            striplength=len(q.strip().replace(' ',''))
                            data['Div_Pay_Date']=q[start:start+striplength+2].replace('.','')
                if i==divyieldtrig:
                    data['Div_Yield']=float(q)
                if i==betatrig:
                    data['Beta']=float(q)

                if i==40:
                    break
                i+=1

        return data
