import json
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os


f=open('../dist/json/portfolio.json')
json_data=json.load(f)
for i in json_data:
    divs=[]
    dates=[]
    annotations=[]
    yields=[]
    if i['DivHistory']!={}:
        price=float(i['price'])

        for z in i['DivHistory']:
            divs.append(i['DivHistory'][z]['Div'])
            dates.append(z)
            annotations.append(i['DivHistory'][z]['Type'])

        for d,a in zip(divs,annotations):
            y=0
            try:
                if a=='M':
                    y=str(round(d*1.0*12/price*100,2))+'%'
                    yields.append(y)
                if a=='Q':
                    y=str(round(d*1.0*4/price*100,2))+'%'
                    yields.append(y)
                if a=='A':
                    y=str(round(d*1.0/price*100,2))+'%'
                    yields.append(y)
            except:
                yields.append('-')
        try:
            plt.rcParams.update({'figure.autolayout': True})
            fig, ax=plt.subplots()
            ax.scatter(dates,divs)
            ax.set(ylim=[0,np.amax(divs)*2], ylabel='$', title=i['ticker']+' Dividends (With Annualized Dividend Yields)')
            for s in range(0,len(divs)):
                if divs[s]<10:
                    scalar=2
                else:
                    scalar=1.2
                ax.annotate(annotations[s],(dates[s],divs[s]*scalar*.95))
                ax.annotate(yields[s],(dates[s],divs[s]*scalar),rotation=45,fontsize=6)

            if len(divs)>10:
                plt.xticks(fontsize=6,rotation=90)
            else:
                plt.xticks(rotation=45)

            plt.subplots_adjust(top=1,bottom=.9)




            file="../dist/portpics/"+i['ticker']+"+divs.png"
            if os.path.isfile(file):
                os.remove(file)
            plt.savefig(file)
            plt.clf()
            plt.close(fig)
        except Exception as e:
            print(e)
            plt.close(fig)
