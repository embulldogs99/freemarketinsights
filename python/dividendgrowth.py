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
            entry['T1LastDiv']=unicorndata['T1Div']
            entry['T1LastDivDate']=unicorndata['T1DivDate']
            entry['T1LastDivType']=unicorndata['T1DivType']
            entry['T2LastDiv']=unicorndata['T2Div']
            entry['T2LastDivDate']=unicorndata['T2DivDate']
            entry['T2LastDivType']=unicorndata['T2DivType']
            entry['T3LastDiv']=unicorndata['T3Div']
            entry['T3LastDivDate']=unicorndata['T3DivDate']
            entry['T3LastDivType']=unicorndata['T3DivType']
            entry['T4LastDiv']=unicorndata['T4Div']
            entry['T4LastDivDate']=unicorndata['T4DivDate']
            entry['T4LastDivType']=unicorndata['T4DivType']
            entry['T5LastDiv']=unicorndata['T5Div']
            entry['T5LastDivDate']=unicorndata['T5DivDate']
            entry['T5LastDivType']=unicorndata['T5DivType']
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
