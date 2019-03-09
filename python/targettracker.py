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
from alphavantage import alphavantagepricepull


warnings.filterwarnings('ignore')

finaldata=[]

try:
    outfile=open('../dist/json/historicalanalysis/targettracker.json','r')
    item=json.load(outfile)
    for i in item:
        finaldata.append(i)
    outfile.close()
except:
    pass


quandl.ApiConfig.api_key = 'omQiMysF2NQ1B-xZEJBk'

def quandl_stocks(symbol, start_date=(2010, 1, 1), end_date=None):
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
			data=float(data)
		except:
			data=int(0)
		price=int(round(data,0))
		if price>1:
			return price


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
            if quandl_adj_close(ticker)>1000:
                s=float(s[0]+s[1])
            else:
                s=float(s[0])
            return s
        except:
            return 0



def spyprice(year,month,day):
    x=pd.read_csv('../SPY.csv')
    if len(month)<2:
        month="0"+month
    if len(day)<2:
        day="0"+day
    date=(str(year)+"-"+str(month)+"-"+str(day))
    price=x['Adj Close'].loc[x['Date']==date].iloc[0]
    if price==None:
        return 0
    else:
        return price



from sqlalchemy import create_engine
from pandas import DataFrame
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

########Create SQL Alchemy Engine Connection##########
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
connection = engine.connect()


start = time.time()
print("beginning analysis")

now = datetime.datetime.now()
lastyear=str(now.year-1)+'-'+str(now.month)+'-'+str(now.day)
months=[6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11,12]
sixmoago=str(now.year)+'-'+str(months[6+now.month-6])+'-'+str(now.day)
today=str(now.year)+'-'+str(now.month)+'-'+str(now.day)
###########
#################################Year-Month-Date
query="Select target, price, returns, ticker, date, note,a_eps, bank from fmi.marketmentions where date='"+lastyear+"' or date='"+sixmoago+"' and report='analyst'"

resoverall = connection.execute(query)
#############Grab Data from SQL Alchemy Execution########################
df=DataFrame(resoverall.fetchall())
########################Rename DF Columns with Keys##########################
df.columns=resoverall.keys()



newindexprice=alphavantagepricepull('SPY')



for index,row in df.iterrows():

    entry={}

    date=str(row['date'])
    postingdate=datetime.datetime.strptime(date,"%Y-%m-%d")
    postingyear=postingdate.year
    postingmonth=postingdate.month
    postingday=postingdate.day

    if postingmonth!=now.month:
        entry['Period']='6mo'
    else:
        entry['Period']='1year'


    entry['AnnouncementDate']=str(row['date'])
    entry['AssessmentDate']=today
    # Define posting date and days



    # determine index return from posting date to today
    # if price is not available, check next day, or next month
    try:
        oldindexprice=spyprice(str(postingyear),str(postingmonth),str(postingday))
    except:
        try:
            oldindexprice=spyprice(str(postingyear),str(postingmonth),str(postingday+1))
        except:
            try:
                oldindexprice=spyprice(str(postingyear),str(postingmonth),str(postingday+2))
            except:
                try:
                    oldindexprice=spyprice(str(postingyear),str(postingmonth),str(postingday+3))
                except:
                    try:
                        oldindexprice=spyprice(str(postingyear),str(postingmonth+1),str(postingday))
                    except:
                        try:
                            oldindexprice=spyprice(str(postingyear),str(postingmonth+1),str(postingday+1))
                        except:
                            oldindexprice=newindexprice

    # having problems with the old found SPY price being zero
    if oldindexprice==0:
        oldindexprice=newindexprice
    if oldindexprice==0:
        oldindexprice=1
    indexreturn=round((float(newindexprice)-float(oldindexprice))/float(oldindexprice),3)

    entry['IndexPrice']=oldindexprice
    entry['IndexReturn']=indexreturn


    bank=row['bank']
    entry['Bank']=bank

    curprice1=float(barchart(row['ticker']))
    curprice2=float(alphavantagepricepull(row['ticker']))

    if curprice2>0 and .9*curprice1 <= curprice2 and curprice2 <= 1.1*curprice1:
        curprice=curprice2
    else:
        curprice=float(row['price'])


    entry['Price']=curprice

    actret=round((curprice-float(row['price']))/float(row['price']),3)
    entry['Return']=actret
    expret=float(row['returns'])
    entry['ExpReturn']=expret
    # determine excess return
    excessreturn=actret-indexreturn
    entry['ExcessReturn']=excessreturn


    if expret>0:
        prediction='bull'
    else:
        prediction='bear'
    entry['Prediction']=prediction

    if excessreturn>0 and expret>0:
        dircalcount=1
    elif excessreturn<0 and expret<0:
        dircalcount=1
    else:
        dircalcount=0

    entry['DirCal']=dircalcount
    finaldata.append(entry)

ofile=open('../dist/json/historicalanalysis/targettracker.json','w')
json.dump(finaldata,ofile)
ofile.close()
