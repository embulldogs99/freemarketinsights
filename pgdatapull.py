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
import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import datetime
#
# os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
# shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")

warnings.filterwarnings('ignore')
#########################################################
##############  Database Connection   ###################



conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
cur = conn.cursor()

# marketbulls
cur.execute("COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(m))) FROM (SELECT * FROM(SELECT DISTINCT on (ticker) target,price,round(returns*100) as returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield FROM fmi.marketmentions WHERE report='analyst' AND bank<>'Other' AND date > current_timestamp - INTERVAL '5 days' ORDER BY ticker,returns DESC) t ORDER BY returns DESC LIMIT 5 ) m)  to 'F:/json/marketbulls.json'")

conn.commit()
print("----------------------------")
print("pulled market bulls")
print("----------------------------")

shutil.move("F:\json\marketbulls.json","dist/json/marketbulls.json")

#MarketBears

cur.execute("COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(m))) FROM (SELECT * FROM(SELECT DISTINCT on (ticker) target,price,round(returns*100) as returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield FROM fmi.marketmentions WHERE report='analyst' AND bank<>'Other' AND date > current_timestamp - INTERVAL '5 days' ORDER BY ticker,returns ASC) t ORDER BY returns ASC LIMIT 5 ) m)  to 'F:/json/marketbears.json'")
conn.commit()
print("----------------------------")
print("pulled market bears")
print("----------------------------")

shutil.move("F:\json\marketbears.json","dist/json/marketbears.json")


#PortfolioHistory
cur.execute("COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(t))) FROM( SELECT to_char(date,'MM/DD/YYYY'),portfolio,snp,nasdaq,portfolioreturn,snpreturn,nasdaqreturn FROM fmi.portfoliohistory) t) to 'F:/json/portfoliohistory.json'")
conn.commit()
print("----------------------------")
print("pulled portfoliohistory")
print("----------------------------")
shutil.move("F:\json\portfoliohistory.json","dist/json/portfoliohistory.json")

#Today Portfolio Movement
cur.execute("COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(t))) FROM( SELECT to_char(date,'MM/DD/YYYY'),portfolio,snp,nasdaq,portfolioreturn,snpreturn,nasdaqreturn FROM fmi.portfoliohistory ORDER BY date DESC LIMIT 1) t) to 'F:/json/portfolioreturn.json'")
conn.commit()
print("----------------------------")
print("pulled portfolioreturn")
print("----------------------------")
shutil.move("F:\json\portfolioreturn.json","dist/json/portfolioreturn.json")


#Portfolio
cur.execute("COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(t))) FROM (SELECT ticker,shares,price,value,target_price,exp_return*100,exp_value,target,to_char(target_date,'MM/DD/YYYY') FROM fmi.portfolio where ticker<>'CASH' ORDER BY exp_return desc) t) to 'F:/json/portfolio.json'")
conn.commit()
print("----------------------------")
print("pulled portfolio")
print("----------------------------")
shutil.move("F:\json\portfolio.json","dist/json/portfolio.json")


#Portfolio Target Trend Database
cur.execute("select ticker from fmi.portfolio")
conn.commit()
stocks=cur.fetchall()
for s in stocks:
    for t in s:
        statement="COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(t))) FROM (select DISTINCT ON (date) target,date,note from fmi.marketmentions where ticker='"+t+"' and report='analyst' order by date desc limit 10) t) to 'F:/json/p"+t+"+targettrend.json'"
        cur.execute(statement)
        shutil.move("F:\json\p"+t+"+targettrend.json","dist/json/"+t+"+targettrend.json")
print("----------------------------")
print("pulled portfolio JSON")
print("----------------------------")




#Portfolio Target Trend Database Images
cur.execute("select ticker from fmi.portfolio")
conn.commit()
stocks=cur.fetchall()

for s in stocks:
    for t in s:
        x=[]
        y=[]

        statement="select DISTINCT ON (date) target,date from fmi.marketmentions where ticker='"+t+"' and report='analyst' and date> (CURRENT_DATE - INTERVAL '1 year') order by date desc"
        cur.execute(statement)
        data=cur.fetchall()

        try:
            for tar,date in data:
                x.append(date)
                y.append(tar)


            plt.rcParams.update({'figure.autolayout': True})
            fig, ax = plt.subplots()
            ax.bar(x, y, align='edge', width=3)

            plt.style.use('fivethirtyeight')
            plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
            ax.set(ylim=[0,np.amax(y)*1.1], xlabel='Date', ylabel='$',title=t+' Target Prices')

            plt.annotate("$"+str(round(np.mean(y),2)),(x[0],np.mean(y)))
            ax.axhline(np.mean(y), ls='--', color='r')
            ax.xaxis_date()


            file="dist/portpics/"+t+"+tt.png"
            if os.path.isfile(file):
                os.remove(file)
            plt.savefig(file)
            plt.clf()

        except Exception as e:
            print(e)
            pass


print("----------------------------")
print("pulled portfolio trend images")
print("----------------------------")



cur.close()
conn.close()
