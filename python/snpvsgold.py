import json
import pandas as pd

f=pd.read_csv('../spxvsgoldata.csv')
f.to_json('../dist/json/spxvsgold.json',orient='records')
