##### Imports #####################

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

###########################################################
##########################################################
######## Used QUANDL Functions #########################

quandl.ApiConfig.api_key = 'omQiMysF2NQ1B-xZEJBk'


def quandl_stocks(symbol, start_date=(2018, 1, 1), end_date=None):
    query_list = ['WIKI' + '/' + symbol + '.' + str(k) for k in range(11, 12)]
    start_date = datetime.date(*start_date)
    if end_date:
        end_date = datetime.date(*end_date)
    else:
        end_date = datetime.date.today()
    return quandl.get(query_list,
            returns='pandas',
            start_date=start_date,
            end_date=end_date,
            collapse='daily',
            order='asc'
            )

def quandl_adj_close(ticker):
	if len(ticker)<5:
		data=pd.DataFrame(quandl_stocks(ticker))
		#data=data[len(data)-1:]
		data=data.tail(1)
		data=str(data.max()).split(' ')[7:8]
		data=re.split(r'[`\-=;\'\\/<>?]', str(data))
		data=data[1]
		try:
			price=float(data)
		except:
			price=None
		return price




def quandl_five_yr_low(ticker):
    if len(ticker)<5:
        data=pd.DataFrame(quandl_stocks_5_year(ticker))
        min=data.min()
        try:
            min=float(min)
            return min
        except:
            pass

###########################################################################
#########Main Barchart Function (ticker puller###############################

def barchart(ticker):
    with requests.Session() as c:
        u='https://www.barchart.com/stocks/quotes/'+ticker
        x=c.get(u)
        x=BeautifulSoup(x.content, "html.parser")
        titles=x.find_all()
        titles=str(titles)
        s=titles[titles.find("dailyLastPrice")+17:titles.find("dailyLastPrice")+17+20].replace('"','').split(",")
        try:
            price=float(s[0])
        except:
            price=None
        return price


########################################################################################
##########################################################################################
###############            YAHOO PE and EPS pullers    ##################################
##########################################################################################

def yahoopepuller(ticker):
	with requests.Session() as c:
		u="http://finance.yahoo.com/quote/"+ticker+"?p=" + ticker
		x=c.get(u)
		x=BeautifulSoup(x.content)
		titles=x.find_all()
		titles=str(titles)
		s=titles.find("PE_RATIO-value")
		pe=titles[s:s+1000]
		sn=pe.find("react-text")
		pe=pe[sn+17:sn+24]
		pe=pe.replace(">","").replace("!","").replace("<","")
		try:
			pe=float(pe)
		except:
			pe=0
		return pe

def yahooepspuller(ticker):
	with requests.Session() as c:
		u="http://finance.yahoo.com/quote/"+ticker+"?p=" + ticker
		x=c.get(u)
		x=BeautifulSoup(x.content)
		titles=x.find_all()
		titles=str(titles)
		s=titles.find("EPS_RATIO-value")
		pe=titles[s:s+1000]
		sn=pe.find("reactid")
		pe=pe[sn+13:sn+18]
		pe=pe.replace(">","").replace("!","").replace("<","").replace("/","").replace('"',"")
		try:
			pe=float(pe)
		except:
			pe=0
		return pe


##############################################################
############ Robinhood API Fucntions #####################
def robinhooddivyield(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['dividend_yield'])

def robinhoodpe(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['pe_ratio'])

def robinhood52high(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['high_52_weeks'])

def robinhood52low(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['low_52_weeks'])

def robinhoodmarketcap(ticker):
    url = "https://api.robinhood.com/fundamentals/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['market_cap'])

def robinhoodprice(ticker):
    url = "https://api.robinhood.com/quotes/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['ask_price'])


################################################################
############ Google API Functions  ##############################

def googlefinancepricepull(ticker):
    url="https://finance.google.com/finance?q="+ticker+"&output=json"
    with requests.Session() as c:
        x=c.get(url)
        x=BeautifulSoup(x.content)
        d=x.find_all()
        d=str(d)
        s=d.find("<b>")
        short=d[s+20:s+2000]
        s2=short.find("<b>")
        short=short[s2:s2+2000]
        s3=short.find("</b>")
        price=short[3:s3]
        try:
            price=float(price)
        except:
            price=0
        return (price)

ticker='NGHC'

print(barchart(ticker))
print(quandl_adj_close(ticker))
print(googlefinancepricepull(ticker))
