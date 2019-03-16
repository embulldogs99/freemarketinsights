# coding: utf-8
######################################################
####################################################
######### Imports #####################

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
from nasdaq import nasdaqpull
from alphavantage import alphavantagepricepull
from unicornpull import unicornpull
from unicornpull import daydeltacalc
import sys
from iexpull import iexstockinfo

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
		time.sleep(60)
		data=pd.DataFrame(quandl_stocks(ticker))
		#data=data[len(data)-1:]
		data=data.tail(1)
		data=str(data.max()).split(' ')[7:8]
		data=re.split(r'[`\-=;\'\\/<>?]', str(data))
		data=data[1]
		try:
			price=float(data)
		except:
			price=0
		return price


def quandl_stocks_5_year(symbol, start_date=(today.year-5, today.month, today.day), end_date=None):
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

def quandl_stocks_1_year(symbol, start_date=(today.year-1, today.month, today.day), end_date=None):
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

def quandl_five_yr_low(ticker):
    if len(ticker)<5:
        data=pd.DataFrame(quandl_stocks_5_year(ticker))
        min=data.min()
        try:
            min=float(min)
            return min
        except:
            pass

def quandl_yr_high(ticker):
    if len(ticker)<5:
        data=pd.DataFrame(quandl_stocks_1_year(ticker))
        max=data.max()
        try:
            max=float(max)
            return max
        except:
            pass

def quandl_yr_low(ticker):
    if len(ticker)<5:
        data=pd.DataFrame(quandl_stocks_1_year(ticker))
        min=data.min()
        try:
            min=float(min)
            return min
        except:
            pass
###########################################################################
#########Main Barchart Function (ticker puller###############################

def barchart(ticker):
    try:
        with requests.Session() as c:
            time.sleep(60)
            u='https://www.barchart.com/stocks/quotes/'+ticker
            x=c.get(u)
            x=BeautifulSoup(x.content, "html.parser")
            titles=x.find_all()
            titles=str(titles)
            s=titles[titles.find("dailyLastPrice")+17:titles.find("dailyLastPrice")+17+20].replace('"','').split(",")
            price=float(s[0])
            return price
    except:
            return 0



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
########### No Longer Work  ###########################
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


################################################################################################
################################################################################################
####### Stock Picker Functions
####### All functions return Arrays of stocks
###########################################################################################
###########################################################################################

def randomstockpick():
    array=[]
    file='../dist/json/tickerlist.json'
    opener=open(file,'r')
    data=json.load(opener)
    for i in range(1,100):
        u=random.choice(data)
        if u.find('^')>0:
            u=u[:u.find('^')]
        array.append(u)
    return array

def randomiexstockpick():
    array=[]
    file='../dist/json/iextickerlist.json'
    opener=open(file,'r')
    data=json.load(opener)
    for i in range(1,100):
        u=random.choice(data)
        array.append(u)
    opener.close()
    return array


def portfoliostockpull():
    # Returns array of portfolio stocks
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("""SELECT ticker,shares,target_price FROM fmi.portfolio where ticker<>'CASH';""")
    portfolio=cur.fetchall()
    array=[]
    for ticker,shares,target_price in portfolio:
        array.append(ticker)
    conn.close()
    return array


######################################################################################################
#####################################################################################################
#####################################################################################################
########### Free Market Insights Market Mentions Data Puller         #################################
##########  Copywright 2019                                       #######################################
##########  Please do not use this code without author's approval   ####################################
##########  Author can be ready via www.freemarketinsights.com    #####################################
########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

now=datetime.datetime.now()

def marketmentions(tickerarray):
    timer=datetime.datetime.now()
    with requests.Session() as c:
        for u in tickerarray:
            value=''
            try:
                url='htt'+'ps://news.google.com/news/rss/search/section/q/'+u+'/'+u+'?hl=en&gl=US&ned=us'
                x=c.get(url)
                x=BeautifulSoup(x.content)
                titles=x.find_all('title')
                pubdate=x.find_all('lastbuilddate')+x.find_all('pubdate')
                for p,t in zip(pubdate,titles):
# Assemble our Output Variable
                    pub=str(p.text)
                    info=str(t.text)
                    if info.find(';')>0:
                        info=info[:info.find(';')]

################################################################################################
###Dynamically determining stock based on text.
# Stock found in RSS feed may not match original stock being search for.

                    stock=info[info.find('(')+1:info.find(')')].replace('NYSE:','').replace('NASDAQ:','').replace('NYSE ','').replace(':','').replace(' ','')

# Once stock is found, make sure the ticker is legitimate and wont cause errors for our other functions
# Also, if we cannot find a target or EPS callout, lets not pull the rest of the other functions
                    if len(stock)>1 and len(stock)<7 and info.find('arget') > 0 or info.find('EPS') >0 or info.find('eps')>0 or info.find('Earnings')>0 or info.find('earnings') > 0:

                        grab=info
    # Define which bank is making the comment
    # Generic Cases
                        bank='Other'
                        if 'Analysts' in grab:
                            bank='Analysts'
                        if 'Brokerages' in grab:
                            bank='Brokerages'
                        if 'Price Target Outlook' in grab:
                            bank='Price Target Outlook'
                        if 'Avg. Price Target Review:' in grab:
                            bank='Avg. Price Target Review'
                        if 'Avg. Price Target Recap:' in grab:
                            bank='Avg. Price Target Recap'
                        if 'Avg. Price Target Opinion:' in grab:
                            bank='Avg. Price Target Opinion'
                        if 'Consensus Target Price' in grab:
                            bank='Consensus Target Price'
                        if 'Price Target Recommendation:' in grab:
                            bank='Price Target Recommendation'
                        if 'Price Target Summary:' in grab:
                            bank='Price Target Summary'
    # Specific Banks or Data Market Information Sites
                        if 'Barclays' in grab:
                            bank='Barclays'
                        if 'Goldman Sachs' in grab:
                            bank='Goldman Sachs'
                        if 'Och-Ziff' in grab:
                            bank='Och-Ziff'
                        if 'Jeffries' in grab:
                            bank='Jeffries'
                        if 'Bank of America' in grab:
                            bank='Bank of America'
                        if 'Piper Jaffray' in grab:
                            bank='Piper Jaffray'
                        if 'Royal Bank of Canada' in grab:
                            bank='Royal Bank of Canada'
                        if 'Cantor Fitzgerald' in grab:
                            bank='Cantor Fitzgerald'
                        if 'Citigroup' in grab:
                            bank='Citigroup'
                        if 'Zacks:' in grab:
                            bank='Zacks'
                        if 'Wells Fargo' in grab:
                            bank='Wells Fargo & Co'
                        if 'Wolfe Research' in grab:
                            bank='Wolfe Research'
                        if 'UBS' in grab:
                            bank='UBS'
                        if 'Telsey Advisory Group' in grab:
                            bank='Telsey Advisory Group'
                        if 'SunTrust Banks' in grab:
                            bank='SunTrust Banks'
                        if 'Stifel Nicolaus' in grab:
                            bank='Stifel Nicolaus'
                        if 'Oppenheimer' in grab:
                            bank='Oppenheimer'
                        if 'Morgan Stanley' in grab:
                            bank='Morgan Stanley'
                        if 'JPMorgan' in grab:
                            bank='JPMorgan'
                        if 'Credit Suisse' in grab:
                            bank='Credit Suisse'
                        if 'Baird' in grab:
                            bank='Baird'
                        if 'Susquehanna' in grab:
                            bank='Susquehanna'
                        if 'Canaccord Genuity' in grab:
                            bank='Canaccord Genuity'
                        if 'B. Riley' in grab:
                            bank='B. Riley'
                        if 'BMO Capital Markets' in grab:
                            bank='BMO Capital Markets'
                        if 'Raymond James' in grab:
                            bank='Raymond James'
                        if 'Deutsche Bank' in grab:
                            bank='Deutsche Bank'
                        if 'Scotiabank' in grab:
                            bank='Scotiabank'
                        if 'BWS Financial' in grab:
                            bank='BWS Financial'
                        if 'HC Wainwright' in grab:
                            bank='HC Wainwright'
    ## Begin filtering the data for model output
    ## First find $$$$
                        if grab.count('$') > 0:
                            targ=int(0)
                            targ=grab.find('$')
                            value=grab[targ+1:targ+5]
    ######## now you have the targeted value, time to clean up
                            if value[2:len(value)].count('-')>0:
                                value=value.replace('-','')
                            if value.endswith('.'):
                                value=value.replace('.','')
                            value=value.replace(' ','')
                            value=value.replace(',','')
                            value=value.replace('k','000')
                            value=value.replace('K','000')
                            value=value.replace('m','000000')
                            value=value.replace('M','000000')
                            value=value.replace('b','000000000')
                            value=value.replace('B','000000000')
                            value=value.replace('T','')
                            value=value.replace(' ','')
                            value=value.replace('in','')
                            value=value.replace('i','')
                            value=value.replace('/','')
                            value=value.replace('S','')
                            value=value.replace('s','')
                            value=value.replace('h','')
                            value=value.replace('a','')
    #try to convert the value into a float
                            try:
                                value=float(value)
#if not a possible float at this point, we will stop trying
# remember floats can be tricky to find and exact decimals often do not have flaoting points. we will try a few tricks to get it to work here
                            except:
                                try:
                                    value=float(value*100)/100
                                except:
                                    try:
                                        value=float(value+.00001)
                                    except:
                                        try:
                                            value=float(value*100000)/100000
                                        except Exception as e:
                                            print("------------------------------------")
                                            print(e)
                                            print(stock)
                                            print("failed to convert value to float with value of:")
                                            print(value)
                                            print("and grab:")
                                            print(grab)
                                            print()
                                            print('error occured at line ~700')
                                            print("------------------------------------")



    # Only selecting stocks we have a value
                            if value>0:
    # Pulling Additional Stock Information
                                try:
                                    iexinfo=iexstockinfo(stock)
                                    yrlow=iexinfo['week52Low']
                                    yrhigh=iexinfo['week52High']
                                    marketcap=iexinfo['marketCap']
                                    peratio=iexinfo['peRatio']
                                    price=iexinfo['latestPrice']
                                except Exception as e:
                                    print('------------------------------------')
                                    print()
                                    print()
                                    print('iexinfo failed to pull')
                                    print()
                                    print(stock)
                                    print()
                                    print(e)
                                    print()
                                    print('------------------------------------')
                                    yrlow=None
                                    yrhigh=None
                                    marketcap=None
                                    peratio=None
                                    price=0
                                try:
                                    epsreference=yahooepspuller(stock)
                                except:
                                    epsreference=None
                                try:
                                    fiveyrlow=quandl_five_yr_low(stock)
                                except:
                                    fiveyrlow=None
                                try:
                                    fiveyrlow=quandl_five_yr_low(stock)
                                except:
                                    fiveyrlow=None

    ######Calling prices to ensure they are available
                                try:
                                    if price==0:
                                        price=alphavantagepricepull(stock)
                                        if price==0:
                                            price=barchart(stock)
                                    price=float(price)
                                except:
                                    print('---------------------------')
                                    print()
                                    print()
                                    print('Could not determine price')
                                    print()
                                    print()
                                    print(stock)
                                    print('-----------------------------')
                                    price=0
    # Grab last dividend
                                try:
                                    divdata=unicornpull(stock)
                                    dividend=divdata['Div']
                                    divyield=divdata['Div']/price
                                except:
                                    divyield=None

    # Finalize on the Annual PE ratio of not available from iex
                                try:
                                    ape=peratio
                                    if peratio==None:
                                        ape=round(price/float(epsreference),2)
                                except Exception as e:
                                    print('-----------------------------------')
                                    print('failed on annual EPS ')
                                    print()
                                    print(e)
                                    print()
                                    print(stock)
                                    print()
                                    print(peratio)
                                    print()
                                    print(grab)
                                    print()
                                    print('-----------------------------------')
                                    ape=0

    # Find EPS callouts
                                if grab.find('EPS') >0 or grab.find('eps')>0 or grab.find('Earnings')>0 or grab.find('earnings') > 0 and price>0:
#determine quarterly PE from the announcement
# sometimes the repoted eps is not able to be converted into a float (due to the fact that not all decimals can be converted into floating point numbers) thus, to avoid the divide by zero error, we try a bunch of tricks
                                    try:
                                        qpe=round(price/float(value),2)
                                    except:
                                        try:
                                            qpe=round(price/float(value+.0000001),2)
                                        except:
                                            try:
                                                qpe=round(price/float(value+.001),2)
                                            except:
                                                try:
                                                    qpe=round(price/float(value*1000)/1000,2)
                                                except:
                                                    qpe=0
    #determine EPS growth rate
    # if variables not availale, so no growth
                                    if epsreference!=0 or epsreference!=None:
                                        epsgrowth=(float(value)*4-epsreference)/abs(epsreference)
                                        targetprice=price+price*epsgrowth/8
                                    else:
                                        epsgrowth=0
                                        targetprice=price
    # determine target price based on EPS growth ranges
                                    if epsgrowth>=2:
                                        targetprice=price*2
                                    if epsgrowth>=1 and epsgrowth<2:
                                        targetprice=price*1.2
                                    if epsgrowth<1 and epsgrowth>=0:
                                        targetprice=price+(price*epsgrowth/8)
                                    if epsgrowth>-1 and epsgrowth<0:
                                        targetprice=price*.8
                                    if epsgrowth<=-1:
                                        targetprice=price/2

                                    epsexpreturn=(targetprice-price)/price

    ##Cleaning Grab (note) to remove "" and / as this will break javascript on html load
                                    grab=grab.replace('"','')
                                    grab=grab.replace('/','')
                                    grab=grab.replace('\\','')
                                    grab=grab.replace('\\\\','')

    #########################################################
    ##############  Database Connection   ###################
                                    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
                                    cur = conn.cursor()
        							# execute a statement
                                    cur.execute("INSERT INTO fmi.marketmentions (target, price, returns, ticker, note, date, q_eps, a_eps, report, q_pe,a_pe, divyield,bank,yrlow,yrhigh,fiveyrlow,earnings_call) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)", (targetprice,price,epsexpreturn,stock,grab,pub,value,epsreference,'earnings',qpe,ape,divyield,bank,yrlow,yrhigh,fiveyrlow,value))
                                    print("----------------------------")
                                    print("inserted value")
                                    conn.commit()
        							# close the communication with the PostgreSQL
                                    cur.close()
                                    conn.close()
                                    currenttime=datetime.datetime.now()-timer
                                    print("Stock "+str(stock)+" Occurred After "+str(currenttime)+" seconds")
                                    print()
                                    print(grab)
                                    print("----------------------------")

# Find price target callouts
                                if grab.find('arget') > 0 and price>0:
# determine price from a variety of sources
# if the expected return is too large, then we will try other stock price sources
                                    predreturn=(float(value)-price)/price
                                    if predreturn>2 or predreturn<-.6:
                                        price=float(alphavantagepricepull(stock))
                                        predreturn=(float(value)-price)/price
                                        if predreturn>2 or predreturn<-.6:
                                            price=float(barchart(stock))
                                            predreturn=(float(value)-price)/price
                                            if predreturn>1 or predreturn<-.8:
                                                price=float(quandl_adj_close(stock))
                                                predreturn=(float(value)-price)/price
                                            else:
                                                price=0

# Now we are pretty confident about the price, assuming it is not absolutely massive or tiny, lets get it into the DB
                                    if price*.1< value and price*10>value:
#########################################################
##############  Database Connection   ###################
                                        conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
                                        cur = conn.cursor()
                                        # execute a statement
                                        cur.execute("INSERT INTO fmi.marketmentions (target, price, returns, ticker, note, date, q_eps, a_eps, report, divyield,bank,yrlow,yrhigh,fiveyrlow) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)", (value,price,predreturn,stock,grab,pub,None,epsreference,'analyst',divyield,bank,yrlow,yrhigh,fiveyrlow))
                                        print("----------------------------")
                                        print("inserted value")
                                        conn.commit()
                                        # close the communication with the PostgreSQL
                                        cur.close()
                                        conn.close()
                                        currenttime=datetime.datetime.now()-timer
                                        print("Stock"+str(stock)+" Occurred After "+str(currenttime)+" seconds")
                                        print()
                                        print(grab)
                                        print("----------------------------")

            except Exception as e:
                print("------------------------------------")
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
                print(e)
                print("Original Stock Name: "+u)
                print("Dynamic Stock Ticker: "+stock)
                print("failed with value of:")
                print(value)
                print("and grab of:")
                print(grab)
                print()
                print("------------------------------------")
                pass


# Define our stock lists that we will want to use
otherstocks=randomstockpick()
iexstocks=randomiexstockpick()
portfoliostocks=portfoliostockpull()

marketmentions(portfoliostocks)
marketmentions(iexstocks)
marketmentions(otherstocks)


print('end')
