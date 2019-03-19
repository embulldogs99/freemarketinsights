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
from iexpull import iexstockinfo

start = time.time()
print("beginning analysis")



warnings.filterwarnings('ignore')



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

pulldate='06-01-2018'

########Create SQL Alchemy Engine Connection##########
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
connection = engine.connect()
###########
#################################Year-Month-Date

# SELECT * FROM (
#     SELECT DISTINCT p.cod, p.title ... JOIN... WHERE
#     ) ORDER BY RANDOM() LIMIT 4;


query="SELECT * FROM( SELECT DISTINCT target, price, returns, ticker, date, note,a_eps, bank from fmi.marketmentions where date<'"+pulldate+"' and report='analyst' ) t ORDER BY random() limit 500"
resoverall = connection.execute(query)
#############Grab Data from SQL Alchemy Execution########################
df=DataFrame(resoverall.fetchall())
########################Rename DF Columns with Keys##########################
df.columns=resoverall.keys()


fdf=DataFrame(columns=('ticker','date','target','price','exp_return','current','act_return','index_return','excess_return','prediction','direction_call_count','note','a_eps','bank'))

insertcount=0


newindexprice=alphavantagepricepull('SPY')

for index,row in df.iterrows():

    time.sleep(3)


    # Define posting date and days
    date=str(row['date'])
    postingdate=datetime.datetime.strptime(date,"%Y-%m-%d")
    postingyear=postingdate.year
    postingmonth=postingdate.month
    postingday=postingdate.day


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
    indexreturn=(float(newindexprice)-float(oldindexprice))/float(oldindexprice)


    bank=row['bank']

    try:
        iexinfo=iexstockinfo(row['ticker'])
        curprice=float(iexinfo['latestPrice'])
    except Exception as e:
        print('--------------------------')
        print('iexinfo failed')
        print()
        print(row['ticker'])
        print()
        print(e)
        print('------------------------------')
        try:
            curprice=float(alphavantagepricepull(row['ticker']))
        except Exception as e:
            print('--------------------------')
            print('alphavantageprice failed')
            print()
            print(row['ticker'])
            print()
            print(e)
            print('------------------------------')
            curprice=float(barchart(row['ticker']))


    actret=(curprice-float(row['price']))/float(row['price'])
    expret=float(row['returns'])
    # determine excess return
    excessreturn=actret-indexreturn


    if expret>0:
        prediction='bull'
    else:
        prediction='bear'

    if excessreturn>0 and expret>0:
        dircalcount=1
    elif excessreturn<0 and expret<0:
        dircalcount=1
    else:
        dircalcount=0


    fdf=fdf.append(pd.Series([row['ticker'],row['date'],float(row['target']),float(row['price']),expret,curprice,actret,indexreturn,excessreturn,prediction,dircalcount,row['note'],float(row['a_eps']),bank], index=fdf.columns), ignore_index=True)
    insertcount=insertcount+1





fdf['ret_delta']=fdf['act_return']-fdf['exp_return']
fdf['excess_ret_delta']=fdf['excess_return']-fdf['exp_return']
fdf['a_eps_score']=(fdf['a_eps']-fdf['a_eps'].mean())/fdf['a_eps'].std()

# select stocks with an actual expected return
fdf=fdf.loc[fdf['act_return'] != 0]
# filter for stocks with an above average annual eps
# fdf=fdf.loc[fdf['a_eps_score'] > 0]

# print(df.loc[df['B'].isin(['one','three'])])

# out to csv
fdf.to_csv('F:/Data/marketmentions_analysis.csv')

#out to json
fdf.to_json('../dist/json/historicalanalysis/historicalanalysis.json', orient='records')


#group by bank and out to file
bankgroup=fdf[['bank','prediction','act_return','exp_return','ret_delta','direction_call_count']]
bankcount=bankgroup.groupby(['bank','prediction'], as_index=False).count()
bankgroupby=bankgroup.groupby(['bank','prediction'], as_index=False).mean()
mergedbanks=pd.merge(bankgroupby,bankcount,left_on=['bank','prediction'], right_on=['bank','prediction'])
mergedbanks['accuracy']=mergedbanks['direction_call_count_x']/mergedbanks['direction_call_count_y']
mergedbanks.to_json('../dist/json/historicalanalysis/bankanalysis.json',orient='table')
# print(fdf.sort_values(by='exp_return',ascending=False).head(20))

# calculate some stats to post on the screen about the analysis

print()
print()
print()
print()
print()
print("---------------------------------------------------")
print("Now Printing Analysis Results")
print("---------------------------------------------------")
print()
print()
print()

print("Average Return Delta")
print(fdf['ret_delta'].mean())
print()
print()


print("Average Excess Return Delta")
print(fdf['excess_ret_delta'].mean())
print()
print()

rowcount=fdf.shape[0]
percentcall=fdf['direction_call_count'].sum()/rowcount
print("% Called Direction")
print(percentcall)
print()
end = time.time()

percentbull=len(fdf[fdf['prediction'] == 'bull'])/rowcount
percentbear=len(fdf[fdf['prediction'] == 'bear'])/rowcount



print("Total elapsed time:"+str(end - start))
print("Inserted "+str(insertcount)+" Values")
print()
print()
print("---------------------------------------------------")
print("End")
print("---------------------------------------------------")



today=datetime.date.today()
todaystring=datetime.datetime.strptime(str(today),"%Y-%m-%d")

analysisarray=[]
analysis={}
analysis['AvgReturnDelta']=fdf['ret_delta'].mean()
analysis['AvgReturn']=fdf['act_return'].mean()
analysis['AvgExReturnDelta']=fdf['excess_ret_delta'].mean()
analysis['AvgExpectedReturn']=fdf['exp_return'].mean()
analysis['PercentCall']=percentcall
analysis['StockCount']=insertcount
analysis['DateRun']=str(today)
analysis['PercentBull']=percentbull
analysis['PercentBear']=percentbear
analysis['PullDate']=str(pulldate)
analysisarray.append(analysis)

outfile=open('../dist/json/historicalanalysis/historicalanalysisstats.json','w')
json.dump(analysisarray,outfile)
outfile.close()
