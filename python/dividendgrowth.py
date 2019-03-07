from nasdaq import nasdaqpull
import json
import decimal
from unicornpull import daydeltacalc
from unicornpull import unicornpull

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

file=open('../dist/json/tempdividend.json','r')
data=json.load(file)
for item in data:
    entry={}
    if item['Ticker']!='-':
        entry['Ticker']=item['Ticker']
        entry['LastPrice']=item['LastPrice']
        entry['Yield']=item['Yield']
        entry['ExDay']=item['ExDay']
        entry['PayDay']=item['PayDay']
        entry['Type']=item['Type']
        entry['Dividend']=item['Dividend']
        entry['DivHistory']=unicornpull(item['Ticker'])
        finaldata.append(entry)
    else:
        pass
        

file.close()
outfile=open('../dist/json/dividendgrowth.json','w')
json.dump(finaldata,outfile)
outfile.close()
