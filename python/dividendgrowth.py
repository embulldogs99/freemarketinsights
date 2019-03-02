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
f.close()

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
            entry['Annual_Dividend']=annualdividend
            if type=='Q':
                dividendgrowth=(dividend*4.0-annualdividend)/annualdividend
                print(dividendgrowth)
            if type=='M':
                dividendgrowth=(dividend*12.0-annualdividend)/annualdividend
            if type=='A':
                dividendgrowth=(dividend-annualdividend)/annualdividend
            entry['Dividend_Growth%']=dividendgrowth
            finaldata.append(entry)
        except:
            annualdividend='-'
            entry['Annual_Dividend']=annualdividend
            entry['Dividend_Growth%']='-'

file.close()
outfile=open('../dist/json/dividendgrowth.json','w')
json.dump(finaldata,outfile)
