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



###########################################################


def barchart(ticker):
    with requests.Session() as c:
        u='https://www.barchart.com/stocks/quotes/'+ticker
        x=c.get(u)
        x=BeautifulSoup(x.content, "html.parser")
        titles=x.find_all()
        titles=str(titles)
        s=titles[titles.find("dailyLastPrice")+17:titles.find("dailyLastPrice")+17+20].replace('"','').split(",")
        if ticker=="GOOGL":
            s=float(s[0]+s[1])
        else:
            s=float(s[0])
        return s

def robinhoodprice(ticker):
    url = "https://api.robinhood.com/quotes/"+ticker+"/"
    headers = {"Accept": "application/json"}
    binary = requests.get(url=url, headers=headers).content
    data=json.loads(binary)
    return float(data['ask_price'])


#############################################################################
############## Pull Current Portfolio and Obtain Tickers  ###################
conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
cur = conn.cursor()
cur.execute("""SELECT ticker,shares,target_price FROM fmi.portfolio where ticker<>'CASH';""")
portfolio=cur.fetchall()


####################################################
###Pull Quandl Price information for each ticker and send it to database#########
###################################################
for ticker,shares,target_price in portfolio:

    try:
        bcprice=barchart(ticker)
        rhprice=robinhoodprice(ticker)
        if bcprice*.9 <= rhprice <= bcprice*1.1:
            price=rhprice
        else:
            price=bcprice
        if bcprice == None:
            price=rhprice
        if rhprice == None:
            price=bcprice
    except:
        price=barchart(ticker)


    value=round(shares*float(price),2)
    cur.execute("""UPDATE fmi.portfolio set price=%s,value=%s where ticker=%s;""", (price, value, ticker))
    conn.commit()

###################################################
####Obtain Recent Market Mentions Analyst projection
###################################################
    cur.execute("""SELECT "target","date" from fmi.marketmentions where ticker='{0}' and report='analyst' order by "date" desc limit 1;""".format(ticker))
    conn.commit()
    marketmentions=cur.fetchall()

    for target,date in marketmentions:
            cur.execute("""UPDATE fmi.portfolio set target=%s,target_date=%s where ticker=%s;""", (target,date,ticker))
            conn.commit()

###########################################
####Insert calculated expected return
##################################################
            exp_return=round((target-price)/float(price),2)
            exp_value=(target*shares)
            cur.execute("""UPDATE fmi.portfolio set exp_return=%s,exp_value=%s where ticker=%s;""", (exp_return,exp_value,ticker))
            conn.commit()

cur.close()
conn.close()
