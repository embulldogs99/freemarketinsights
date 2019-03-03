import requests
import pandas as pd
from bs4 import BeautifulSoup

with requests.Session() as c:
    x=c.get('https://www.usinflationcalculator.com/inflation/historical-inflation-rates/')
    soup=BeautifulSoup(x.content)
    data=soup.find_all('table')
    datarows=data[0].find_all('tr')


    entry={}
    counter=0
    for i in datarows:
        for data in i:
            data=str(data)
            print(data[data.find('>')+1:data[data.find('>'):].find('<')])
        #     if counter==0:
        #         year=data
        #         counter+=1
        #     else:
        #         entry[year]=data
        #         counter+=1
        # counter=0
    print(entry)
    # datarows=data[0].find_all('td')
    # columns=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    # entry={}
    # count=0
    # for i in datarowdates:
    #     for d in datarows:
    #         if count>len(columns+1):
    #             print(i)
    #     count+=1
