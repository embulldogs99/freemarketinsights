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
        entry['Type']=item['Type']
        entry['Dividend']=item['Dividend']
        try:
            unicorndata=unicornpull(item['Ticker'])
            entry['LastDiv']=unicorndata['Div']
            entry['LastDivDate']=unicorndata['DivDate']
            entry['LastDivType']=unicorndata['DivType']
            entry['DivHistory']=unicorndata
        except:
            entry['LastDiv']={}
            entry['LastDivDate']={}
            entry['LastDivType']={}
            entry['DivHistory']={}

        finaldata.append(entry)
    else:
        pass

file.close()
outfile=open('../dist/json/dividendgrowth.json','w')
json.dump(finaldata,outfile)
outfile.close()
