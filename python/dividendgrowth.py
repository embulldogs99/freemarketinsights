from nasdaq import nasdaqpull
import json
import decimal


finaldata=[]
growthfile='../dist/json/dividendgrowth.json'
f=open(growthfile,'r')
try:
    fdata=json.load(f)
    for i in fdata:
        finaldata.append(i)
except:
    pass


file=open('../dist/json/dividend.json','r')
data=json.load(file)
for item in data:
    entry={}
    if item['Ticker']!='-':
        ticker=item['Ticker']
        entry['Ticker']=ticker
        type=item['Type']
        entry['Type']=type
        dividend=decimal.Decimal(item['Dividend'])
        entry['Dividend']=float(dividend)
        try:
            nasdaqdata=nasdaqpull(ticker)
            annualdividend=decimal.Decimal(nasdaqdata['Anul_Div'])
            entry['Annual_Dividend']=float(annualdividend)
        except:
            annualdividend='-'
            entry['Annual_Dividend']=annualdividend
        if annualdividend=='-':
            dividendgrowth='-'
        else:
            if type=='Q':
                dividendgrowth=round(float((((dividend+dividend+dividend+dividend)-annualdividend)/annualdividend))*100.0,3)
            if type=='M':
                dividendgrowth=round((dividend*12-annualdividend)/annualdividend,3)
            if type=='A':
                dividendgrowth=round((dividend-annualdividend)/annualdividend,3)

        entry['Dividend_Growth%']=str(dividendgrowth)
        if entry['Dividend_Growth%']!='-':
            finaldata.append(entry)

outfile=open('../dist/json/dividendgrowth.json','w')
json.dump(finaldata,outfile)
