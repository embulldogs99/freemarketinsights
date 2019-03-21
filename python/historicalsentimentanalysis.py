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
from sqlalchemy import create_engine
from pandas import DataFrame


start = time.time()
print("beginning analysis")



warnings.filterwarnings('ignore')



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


def spyprice(year,month):
    year=str(year)
    month=str(month)
    if year.find('.')>0:
        year=year[:year.find('.')]
    if month.find('.')>0:
        month=month[:month.find('.')]
    x=pd.read_csv('../SPY.csv')
    date=(month+'-'+year)
    price=x['Adj Close'].loc[x['M_Y_Date']==date].iloc[0]
    if price==None:
        return 0
    else:
        return price



pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

pulldate='06-01-2018'

########Create SQL Alchemy Engine Connection##########
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
connection = engine.connect()
###########
#################################Year-Month-Date

# Raise Query
query="select DISTINCT ticker,date_part('month',date) as month, date_part('year',date) as year,price,a_eps,returns,bank,note from fmi.marketmentions where to_tsvector(note) @@ to_tsquery('raise') and report='analyst' and date<'"+pulldate+"'"
resoverall = connection.execute(query)
df1=DataFrame(resoverall.fetchall())
df1.columns=resoverall.keys()
df1['sentiment']='positive'
df1['trigger_word']='raise'
# Raise Query
query="select DISTINCT ticker,date_part('month',date) as month, date_part('year',date) as year,price,a_eps,returns,bank,note from fmi.marketmentions where to_tsvector(note) @@ to_tsquery('boost') and report='analyst' and date<'"+pulldate+"'"
resoverall = connection.execute(query)
df2=DataFrame(resoverall.fetchall())
df2.columns=resoverall.keys()
df2['sentiment']='positive'
df2['trigger_word']='boost'
# Raise Query
query="select DISTINCT ticker,date_part('month',date) as month, date_part('year',date) as year,price,a_eps,returns,bank,note from fmi.marketmentions where to_tsvector(note) @@ to_tsquery('lower') and report='analyst' and date<'"+pulldate+"'"
resoverall = connection.execute(query)
df3=DataFrame(resoverall.fetchall())
df3.columns=resoverall.keys()
df3['sentiment']='negative'
df3['trigger_word']='lower'


frames=[df1,df2,df3]
sdf=pd.concat(frames)


fdf=DataFrame(columns=('ticker','month','year','price','a_eps','exp_return','bank','note','sentiment','trigger_word','current','act_return','index_return','excess_return','prediction','direction_call_count','rowcount'))


insertcount=0
newindexprice=alphavantagepricepull('SPY')
for index,row in sdf.iterrows():

    oldindexprice=spyprice(row['year'],row['month'])

    # having problems with the old found SPY price being zero
    if oldindexprice==0:
        oldindexprice=newindexprice
    if oldindexprice==0:
        oldindexprice=1
    indexreturn=(float(newindexprice)-float(oldindexprice))/float(oldindexprice)


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

    dircalcount=0
    if actret>0 and expret>0:
        dircalcount=1
    if actret<0 and expret<0:
        dircalcount=1



    fdf=fdf.append(pd.Series([row['ticker'],row['month'],row['year'],float(row['price']),float(row['a_eps']),expret,row['bank'],row['note'],row['sentiment'],row['trigger_word'],curprice,actret,indexreturn,excessreturn,prediction,dircalcount,1], index=fdf.columns), ignore_index=True)
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
fdf.to_csv('F:/Data/marketmentions_sentimentanalysis.csv')

#out to json
fdf.to_json('../dist/json/historicalanalysis/historicalsentimentanalysis.json', orient='records')


# Calculate Bank stats by sentiment
bankgroup=fdf[['bank','prediction','sentiment','trigger_word','act_return','exp_return','ret_delta','direction_call_count','rowcount']]
bankgroupby=bankgroup[['bank','sentiment','trigger_word','act_return','exp_return','ret_delta']].groupby(['bank','sentiment'], as_index=False).mean()
bankgroupsum=bankgroup[['bank','sentiment','direction_call_count','rowcount']].groupby(['bank','sentiment'], as_index=False).sum()
mergedbanks=pd.merge(bankgroupby,bankgroupsum,left_on=['bank','sentiment'], right_on=['bank','sentiment'])
mergedbanks['accuracy']=mergedbanks['direction_call_count']/mergedbanks['rowcount']
mergedbanks.to_json('../dist/json/historicalanalysis/sentimentbankanalysis.json',orient='table')

# Calculate average bank performance
banksummary1=mergedbanks[['bank','act_return','exp_return']].groupby(['bank'], as_index=False).mean()
banksummary2=mergedbanks[['bank','direction_call_count','rowcount']].groupby(['bank'], as_index=False).sum()
banksummary=pd.merge(banksummary1,banksummary2,left_on=['bank'],right_on=['bank'])
banksummary['accuracy']=banksummary['direction_call_count']/banksummary['rowcount']
banksummary.to_json('../dist/json/historicalanalysis/sentimentbanksummary.json',orient='table')

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
analysis['AvgBankAccuracy']=banksummary['accuracy'].mean()
analysis['PercentCall']=percentcall
analysis['StockCount']=insertcount
analysis['DateRun']=str(today)
analysis['PercentBull']=percentbull
analysis['PercentBear']=percentbear
analysis['PullDate']=str(pulldate)
analysisarray.append(analysis)

outfile=open('../dist/json/historicalanalysis/historicalsentimentanalysisstats.json','w')
json.dump(analysisarray,outfile)
outfile.close()
