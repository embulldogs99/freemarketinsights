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
