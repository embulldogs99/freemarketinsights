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
filename="dist/json/marketbulls.json"
fileread=open(filename,"r")
filestring=fileread.read()
filestring=str(filestring).replace("\\\\","")
filestring=str(filestring).replace("\\\","")
filestring=str(filestring).replace("\\","")
filestring=str(filestring).replace('"',"")
filestring=str(filestring).replace('"Buy"','Buy')
filestring=str(filestring).replace('"Sell"','Sell')
filestring=str(filestring).replace('"Hold"','Hold')
filestring=str(filestring).replace('"Outperform"','Outperform')
fileread.close()
filewrite=open(filename,"w")
filewrite.write(filestring)
filewrite.close()



#MarketBears

cur.execute("COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(m))) FROM (SELECT * FROM(SELECT DISTINCT on (ticker) target,price,round(returns*100) as returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield FROM fmi.marketmentions WHERE report='analyst' AND bank<>'Other' AND date > current_timestamp - INTERVAL '5 days' ORDER BY ticker,returns ASC) t ORDER BY returns ASC LIMIT 5 ) m)  to 'F:/json/marketbears.json'")
conn.commit()
print("----------------------------")
print("pulled market bears")
print("----------------------------")

shutil.move("F:\json\marketbears.json","dist/json/marketbears.json")
filename2="dist/json/marketbears.json"
fileread2=open(filename2,"r")
filestring2=fileread2.read()
filestring2=str(filestring2).replace("\\\\","")
filestring2=str(filestring2).replace("\\\","")
filestring2=str(filestring2).replace("\\","")
filestring2=str(filestring2).replace('"',"")
filestring2=str(filestring2).replace('"Buy"','Buy')
filestring2=str(filestring2).replace('"Sell"','Sell')
filestring2=str(filestring2).replace('"Hold"','Hold')
filestring2=str(filestring2).replace('"Outperform"','Outperform')
fileread2.close()
filewrite2=open(filename2,"w")
filewrite2.write(filestring2)
filewrite2.close()



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
        statement="COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(t))) FROM (select DISTINCT ON (date) target,date,note from fmi.marketmentions where ticker='"+t+"' and report='analyst' and date> (CURRENT_DATE - INTERVAL '1 year') order by date desc) t) to 'F:/json/targettrend"+t+".json'"
        cur.execute(statement)
        shutil.move("F:\json\targettrend"+t+".json","dist/json/"+t+"+targettrend.json")
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
        b=[]
        p=[]

        statement="select DISTINCT ON (date) target,date,bank from fmi.marketmentions where ticker='"+t+"' and report='analyst' and date> (CURRENT_DATE - INTERVAL '1 year') order by date desc"
        cur.execute(statement)
        data=cur.fetchall()

        try:
            for tar,date,bank in data:
                x.append(date)
                y.append(tar)
                if bank=='Analysts' or bank=='Other' or bank=='Zacks' or bank=='Price Target Review' or bank=='Price Target Recommendation' or bank=='Brokerages' or bank=='Price Target Summary' or bank=='Consensus Target Price' or bank=='Avg. Price Target Opinion' or bank=='Avg. Price Target Recap' or bank=="Avg. Price Target Review" or bank=='Avg. Price Target Opinion' or bank=='Price Target Outlook':
                    b.append('')
                else:
                    b.append(bank)

                statement2="select DISTINCT price from fmi.portfolio where ticker='"+t+"'"

                cur.execute(statement2)
                prices=cur.fetchall()
                for price in prices:
                    p.append(price[0])


            plt.rcParams.update({'figure.autolayout': True})
            fig, ax = plt.subplots()
            ax.bar(x, y, align='edge', width=3)
            ax.set_facecolor("white")

            plt.style.use('fivethirtyeight')
            plt.setp(ax.get_xticklabels(), rotation=90, horizontalalignment='right')
            ax.set(ylim=[0,np.amax(y)*1.1], xlabel='Date', ylabel='$',title=t+' Target Prices')

            halfway=int(round(len(x)*.2,0))
            for i in range(0,len(x)):
                if b[i]!='':
                    plt.annotate(str(b[i])+'@ $'+str(y[i]),(x[i],y[i]*random.random()),size=8)

            plt.annotate("Avg Target $"+str(round(np.mean(y),2)),(x[-1],np.mean(y)*1.2))
            plt.annotate("LP $"+str(round(p[0],2)),(x[halfway],np.mean(y)*1.1))

            ax.axhline(np.mean(y), ls='--', color='r')
            ax.axhline(p[0], ls='--', color='g')
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
