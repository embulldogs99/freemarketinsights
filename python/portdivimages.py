import json
f=open('../dist/json/portfolio.json')
json_data=json.load(f)
for i in json_data:
    divs=[]
    dates=[]
    annotations=[]
    if i['DivHistory']!={}:
        divs.append(i['DivHistory']['Div'])
        dates.append(i['DivHistory']['DivDate'])
        annotations.append(i['DivHistory']['DivType'])
        divs.append(i['DivHistory']['T1Div'])
        dates.append(i['DivHistory']['T1DivDate'])
        annotations.append(i['DivHistory']['T1DivType'])
        divs.append(i['DivHistory'][T2'Div'])
        dates.append(i['DivHistory']['T2DivDate'])
        annotations.append(i['DivHistory']['T2DivType'])
        divs.append(i['DivHistory']['T3Div'])
        dates.append(i['DivHistory']['T3DivDate'])
        annotations.append(i['DivHistory']['T3DivType'])
        divs.append(i['DivHistory']['T4Div'])
        dates.append(i['DivHistory']['T4DivDate'])
        annotations.append(i['DivHistory']['T4DivType'])
        divs.append(i['DivHistory']['T5Div'])
        dates.append(i['DivHistory']['T5DivDate'])
        annotations.append(i['DivHistory']['T5DivType'])
    print(i['DivHistory'])
