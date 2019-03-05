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
        divs.append(i['DivHistory']['T5Div'])
        dates.append(i['DivHistory']['T5DivDate'])
        annotations.append(i['DivHistory']['T5DivType'])

        divs.append(i['DivHistory']['T4Div'])
        dates.append(i['DivHistory']['T4DivDate'])
        annotations.append(i['DivHistory']['T4DivType'])

        divs.append(i['DivHistory']['T3Div'])
        dates.append(i['DivHistory']['T3DivDate'])
        annotations.append(i['DivHistory']['T3DivType'])

        divs.append(i['DivHistory']['T2Div'])
        dates.append(i['DivHistory']['T2DivDate'])
        annotations.append(i['DivHistory']['T2DivType'])

        divs.append(i['DivHistory']['T1Div'])
        dates.append(i['DivHistory']['T1DivDate'])
        annotations.append(i['DivHistory']['T1DivType'])

        divs.append(i['DivHistory']['Div'])
        dates.append(i['DivHistory']['DivDate'])
        annotations.append(i['DivHistory']['DivType'])


        for d in divs:
            y=0
            y=str(round(d*1.0/i['price']*100,2))+'%'
            yields.append(y)

        try:
            plt.rcParams.update({'figure.autolayout': True})
            fig, ax=plt.subplots()
            ax.scatter(dates,divs)
            ax.set(ylim=[0,np.amax(divs)*2], ylabel='$', title=i['ticker']+' Dividends')
            for s in range(0,len(divs)):
                ax.annotate(annotations[s],(dates[s],divs[s]*1.05))
                ax.annotate(yields[s],(dates[s],divs[s]*1.2))

            file="../dist/portpics/"+i['ticker']+"+divs.png"
            if os.path.isfile(file):
                os.remove(file)
            plt.savefig(file)
            plt.clf()
        except Exception as e:
            print(e)
