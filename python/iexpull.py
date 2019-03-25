import requests
import json

def iextickerlist():
    url="https://api.iextrading.com/1.0/ref-data/symbols"
    r=requests.get(url)
    jsondata=json.loads(r.text)
    array=[]
    for i in jsondata:
        array.append(i['symbol'])
    outfile=open('../dist/json/iextickerlist.json','w')
    json.dump(array,outfile)
    outfile.close()

def iexstockinfo(ticker):
    url="https://api.iextrading.com/1.0/stock/"+ticker+"/book"
    r=requests.get(url)
    jsondata=json.loads(r.text)
    data=jsondata['quote']
    return data

def iexstockdivyield(ticker):
    url="https://cloud.iexapis.com/beta/stock/"+ticker+"/stats?token=pk_ea5eff50ab824d8c90e20a37c8aa0920"
    r=requests.get(url)
    jsondata=json.loads(r.text)
    data=jsondata['dividendYield']
    return data

def iexstockstats(ticker):
    url="https://cloud.iexapis.com/beta/stock/"+ticker+"/stats?token=pk_ea5eff50ab824d8c90e20a37c8aa0920"
    r=requests.get(url)
    jsondata=json.loads(r.text)
    data=jsondata
    return data

# {"week52change":-0.343195,"week52high":10,"week52low":3.75,"marketcap":83005800,"employees":null,"day200MovingAvg":6.96,"day50MovingAvg":5.14,"float":14020551,"avg10Volume":381109.8,"avg30Volume":167245.5,"ttmEPS":null,"ttmDividendRate":null,"companyName":"Build-A-Bear Workshop, Inc.","sharesOutstanding":14956000,"maxChangePercent":-0.778443,"year5ChangePercent":-0.394105,"year2ChangePercent":-0.354651,"year1ChangePercent":-0.343195,"ytdChangePercent":0.284722,"month6ChangePercent":-0.365714,"month3ChangePercent":0.415816,"month1ChangePercent":0.088235,"day30ChangePercent":0.105578,"day5ChangePercent":0,"nextDividendRate":null,"dividendYield":null,"peRatio":null,"nextEarningsDate":"2019-06-03","exDividendDate":null}

def iexbalancesheet(ticker):
    url='https://cloud.iexapis.com/beta/stock/'+ticker+'/balance-sheet?period=annual&'
    r=requests.get(url)
    jsondata=json.loads(r.text)
    data=jsondata['balancesheet']
    return data

# {"symbol":"AAPL","balancesheet":[{"reportDate":"2018-09-30","currentCash":25913000000,"shortTermInvestments":40388000000,"receivables":23186000000,"inventory":3956000000,"otherCurrentAssets":12087000000,"currentAssets":131339000000,"longTermInvestments":170799000000,"propertyPlantEquipment":41304000000,"goodwill":null,"intangibleAssets":null,"otherAssets":22283000000,"totalAssets":365725000000,"accountsPayable":55888000000,"currentLongTermDebt":8784000000,"otherCurrentLiabilities":40230000000,"totalCurrentLiabilities":116866000000,"longTermDebt":93735000000,"otherLiabilities":4268000000,"minorityInterest":0,"totalLiabilities":258578000000,"commonStock":40201000000,"retainedEarnings":70400000000,"treasuryStock":null,"capitalSurplus":null,"shareholderEquity":107147000000,"netTangibleAssets":107147000000}]}


def iexcashflow(ticker):
    url='https://cloud.iexapis.com/beta/stock/'+ticker+'/cash-flow?period=annual&token=pk_ea5eff50ab824d8c90e20a37c8aa0920'
    r=requests.get(url)
    jsondata=json.loads(r.text)
    data=jsondata['cashflow']
    return data

# {"symbol":"AAPL","cashflow":[{"reportDate":"2018-09-30","netIncome":59531000000,"depreciation":10903000000,"changesInReceivables":-5312000000,"changesInInventories":828000000,"cashChange":5624000000,"cashFlow":77434000000,"capitalExpenditures":-13313000000,"investments":30845000000,"investingActivityOther":-745000000,"totalInvestingCashFlows":16066000000,"dividendsPaid":-13712000000,"netBorrowings":432000000,"otherFinancingCashFlows":-2527000000,"cashFlowFinancing":-87876000000,"exchangeRateEffect":null}]}


def iexearnings(ticker):
    url='https://cloud.iexapis.com/beta/stock/'+ticker+'/earnings/4?token=pk_ea5eff50ab824d8c90e20a37c8aa0920'
    r=requests.get(url)
    jsondata=json.loads(r.text)
    data=jsondata['earnings']
    return data

#
# {"symbol":"AAPL","earnings":[{"actualEPS":4.18,"consensusEPS":4.66,"announceTime":"AMC","numberOfEstimates":36,"EPSSurpriseDollar":-0.48,"EPSReportDate":"2019-01-29","fiscalPeriod":"Q4 2018","fiscalEndDate":"2018-12-31","yearAgo":3.89,"yearAgoChangePercent":0.0746},{"actualEPS":2.91,"consensusEPS":2.76,"announceTime":"AMC","numberOfEstimates":36,"EPSSurpriseDollar":0.15,"EPSReportDate":"2018-11-01","fiscalPeriod":"Q3 2018","fiscalEndDate":"2018-09-30","yearAgo":2.07,"yearAgoChangePercent":0.4058},{"actualEPS":2.34,"consensusEPS":2.16,"announceTime":"AMC","numberOfEstimates":34,"EPSSurpriseDollar":0.18,"EPSReportDate":"2018-07-31","fiscalPeriod":"Q2 2018","fiscalEndDate":"2018-06-30","yearAgo":1.67,"yearAgoChangePercent":0.4012},{"actualEPS":2.73,"consensusEPS":2.71,"announceTime":"AMC","numberOfEstimates":30,"EPSSurpriseDollar":0.02,"EPSReportDate":"2018-05-01","fiscalPeriod":"Q1 2018","fiscalEndDate":"2018-03-31","yearAgo":2.1,"yearAgoChangePercent":0.3}]}
#
#

def iexfundamentals(ticker):
    data={}

    quote=iexstockinfo(ticker)
    data['price']=quote['latestPrice']

    stats=iexstockstats(ticker)
    marketcap=stats['marketcap']
    data['marketcap']=marketcap

    cashflow=iexcashflow(ticker)
    balancesheet=iexbalancesheet(ticker)
    data['roa']=cashflow['netIncome']/balancesheet['totalAssets']
    data['roe']=cashflow['netIncome']/balancesheet['shareholderEquity']
    data['debttoequity']=(balancesheet['LongTermDebt']+balancesheet['currentLongTermDebt'])/balancesheet['shareholderEquity']
    data['debttomarket']=(balancesheet['LongTermDebt']+balancesheet['currentLongTermDebt'])/marketcap


    earnings=iexearnings(ticker)
    eps=[]
    epschange=[]
    epssurprise=[]
    epsdate=[]
    for i in len(earnings):
        eps.append(i['actualEPS'])
        epssurprise.append(i['EPSSurpriseDollar'])
        epsdate.append(i['EPSReportDate'])
        epschange.append(i['yearAgoChangePercent'])
        if i==0:
            data['earningsyoygrowth']=i['yearAgoChangePercent']

    change=1
    for z in epschange:
        change=change+change*z

    data['avgepsgrowth']=(change-1)/len(epschange)


    outfile=open('../dist/json/recentfundamentals.json','w')
    json.dump(data,outfile)
    outfile.close()

import pandas as pd
def iexdataanalysis():
    startdata=pd.read_json('../dist/json/recentfundamentals.json')
    df=pd.DataFrame(startdata)
    print df
