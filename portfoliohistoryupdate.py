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
from decimal import *



def portfoliohistoryduplicatedelete():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()

    cur.execute("CREATE TABLE fmi.portfoliohistory_temp (LIKE fmi.portfoliohistory);")
    conn.commit()
    cur.execute("INSERT into fmi.portfoliohistory_temp(date,portfolio,snp,nasdaq,portfolioreturn,snpreturn,nasdaqreturn) SELECT DISTINCT ON (date) date,portfolio,snp,nasdaq,portfolioreturn,snpreturn,nasdaqreturn FROM fmi.portfoliohistory;")
    conn.commit()
    cur.execute("DROP TABLE fmi.portfoliohistory;")
    conn.commit()
    cur.execute("ALTER TABLE fmi.portfoliohistory_temp RENAME TO portfoliohistory;")
    conn.commit()
    # close the communication with the PostgreSQL
    cur.close()
    conn.close()

##################################
######## QUANDL Functions #########################

quandl.ApiConfig.api_key = 'omQiMysF2NQ1B-xZEJBk'

def barchart_snp500():
    with requests.Session() as c:
        u='https://www.barchart.com/stocks/quotes/$SPX'
        x=c.get(u)
        x=BeautifulSoup(x.content, "html.parser")
        titles=x.find_all()
        titles=str(titles)
        s=titles[titles.find("dailyLastPrice")+17:titles.find("dailyLastPrice")+17+10].replace('"','').replace(",","")
        try:
            s=float(s)
            return s
        except:
            return 0

def barchart_nasdaq():
    with requests.Session() as c:
        u='https://www.barchart.com/etfs-funds/quotes/QQQ'
        x=c.get(u)
        x=BeautifulSoup(x.content, "html.parser")
        titles=x.find_all()
        titles=str(titles)
        s=titles[titles.find("dailyLastPrice")+17:titles.find("dailyLastPrice")+17+8].replace('"','').replace(",","")
        return float(s)

#############################################################################
############## Pull Current Portfolio and Obtain Tickers  ###################
def portfoliovalue():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("""SELECT SUM(value) as total FROM fmi.portfolio;""")
    portfoliovalues=cur.fetchall()
    for row in portfoliovalues:
        portfoliovalue=row
    snpvalue=barchart_snp500()
    nasdaqvalue=barchart_nasdaq()
    now=datetime.datetime.now()
    currentdate=now.strftime("%Y-%m-%d")

    cur.execute("""INSERT INTO fmi.portfoliohistory (date,portfolio,snp,nasdaq) VALUES (%s,%s,%s,%s);""", (currentdate,portfoliovalue,snpvalue,nasdaqvalue))
    cur.execute("""UPDATE fmi.portfoliohistory set portfolio=%s, snp=%s, nasdaq=%s where date=%s;""", (portfoliovalue,snpvalue,nasdaqvalue,currentdate))
    conn.commit()
    cur.close()
    conn.close()

def portfoliohistoryreturnscalc():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("""SELECT DISTINCT on (date) date,portfolio,snp,nasdaq,portfolioreturn,snpreturn,nasdaqreturn FROM fmi.portfoliohistory ORDER BY date asc;""")
    portfolio=cur.fetchall()
    row=0
    for d,p,s,n,pr,sr,nr in portfolio:
        if row==0:
            pastport=p
            pastsnp=s
            pastnasdaq=n
            cur.execute("""UPDATE fmi.portfoliohistory set portfolioreturn=%s, snpreturn=%s, nasdaqreturn=%s WHERE date=%s;""", (0,0,0,d))
            conn.commit()
            row+=1
        else:
            portfolioreturn=round((p-pastport)/Decimal(pastport),4)
            snpreturn=round((s-pastsnp)/Decimal(pastsnp),4)
            nasdaqreturn=round((n-pastnasdaq)/Decimal(pastnasdaq),4)
            pastport=p
            pastsnp=s
            pastnasdaq=n
            row+=1
            cur.execute("""UPDATE fmi.portfoliohistory set portfolioreturn=%s, snpreturn=%s, nasdaqreturn=%s WHERE date=%s;""", (portfolioreturn,snpreturn,nasdaqreturn,d))
            conn.commit()
    cur.close()
    conn.close()


def portfoliohistorycumcalc():
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("""SELECT DISTINCT on (date) date,portfolioreturn,snpreturn,nasdaqreturn,cumport,cumsnp,cumnasdaq FROM fmi.portfoliohistory ORDER BY date asc;""")
    portfolio=cur.fetchall()
    row=0
    for d,pr,sr,nr,cp,cs,cr in portfolio:
        if row==0:
            pastcumport=1
            pastcumsnp=1
            pastcumnasdaq=1
            cur.execute("""UPDATE fmi.portfoliohistory set cumport=%s, cumsnp=%s, cumnasdaq=%s WHERE date=%s;""", (1,1,1,d))
            conn.commit()
            row+=1
        else:
            cumport=round(pastcumport+(pastcumport*pr),6)
            cumsnp=round(pastcumsnp+(pastcumsnp*sr),6)
            cumnasdaq=round(pastcumnasdaq+(pastcumnasdaq*nr),6)

            pastcumport=cumport
            pastcumsnp=cumsnp
            pastcumnasdaq=cumnasdaq

            row+=1
            cur.execute("""UPDATE fmi.portfoliohistory set cumport=%s, cumsnp=%s, cumnasdaq=%s WHERE date=%s;""", (cumport,cumsnp,cumnasdaq,d))
            conn.commit()
    cur.close()
    conn.close()

portfoliovalue()
portfoliohistoryduplicatedelete()
portfoliohistoryreturnscalc()
portfoliohistorycumcalc()
