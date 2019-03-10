import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from alphavantage import alphavantagepricepull
import datetime

finaldata={}
startfile=open('../dist/json/goldpricez.json','r')
startdata=json.load(startfile)
counter=0
for i in startdata:
    if counter==0:
        finaldata['T1']=startdata[i]
        counter+=1
url='http://goldpricez.com/api/rates/currency/sar/measure/all'
headers={"X-API-Key":"998732c1785a2d87cfc3c60313f78397998732c1"}
r=requests.get(url,headers=headers)
j=r.text.replace('\\','')
jsonable=j[1:len(j)-1]
jsondata=json.loads(jsonable)

entry={}
date={}
for i in jsondata:
    entry[i]=jsondata[i]

entry['spx_gold']=round(float(alphavantagepricepull('SPX'))/float(jsondata['ounce_price_usd']),3)

finaldata['T']=entry

outfile=open('../dist/json/goldpricez.json','w')
json.dump(finaldata,outfile)
outfile.close()
