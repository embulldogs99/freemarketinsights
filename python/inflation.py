import requests
import pandas as pd
from bs4 import BeautifulSoup

with requests.Session() as c:
    x=c.get('https://www.usinflationcalculator.com/inflation/historical-inflation-rates/')
    soup=BeautifulSoup(x.content)
    data=soup.find_all('table')

    datarows=data[0].find_all('tr')
    dataheads=data[0].find_all('th')
    heads=[]
    count=0
    for h in dataheads:
        if count>12:
            heads.append(h)

    columns=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    entry={}

    for i,y,b in zip(datarows,heads,columns):
        datas=i.find_all('td')
        for d in datas:
            d=str(d)
            first=d.find('>')
            if first>0:
                last=data[first+1:].find('<')
                finaldata=data[first+1:first+1+last]
                entry[y]=finaldata

    print(entry)

            # print(data[data.find('>')+1:data[data.find('>'):].find('<')])
        #     if counter==0:
        #         year=data
        #         counter+=1
        #     else:
        #         entry[year]=data
        #         counter+=1
        # counter=0
    print(entry)
    # datarows=data[0].find_all('td')

    # entry={}
    # count=0
    # for i in datarowdates:
    #     for d in datarows:
    #         if count>len(columns+1):
    #             print(i)
    #     count+=1
