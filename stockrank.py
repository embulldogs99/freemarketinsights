import psycopg2
from pandas import DataFrame
import pandas as pd
from sqlalchemy import create_engine

#######################################################################################################
############################# Analyst Price Target Report Filter #####################################
#################################################################################################

########Create SQL Alchemy Engine Connection##########
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
connection = engine.connect()
###########
query="Select DISTINCT ON (ticker) target,price, returns, ticker, date(date), q_eps, a_eps, report, note, divyield,yrlow,yrhigh,fiveyrlow from fmi.marketmentions WHERE date > (current_date - 30) AND report='analyst' ORDER BY ticker,date desc"
resoverall = connection.execute(query)

#############Grab Data from SQL Alchemy Execution########################
df=DataFrame(resoverall.fetchall())

########################Rename DF Columns with Keys##########################
df.columns=resoverall.keys()

#########Only looking at stockw tih positive Expected Target Prices per brokerages
df=df[df['returns']>0]

########## Calcing Additional Columns
df['ret/p']=df['returns']/df['price']
df['ret/p'].astype(float).round(2)
df['a_e/p']=df['a_eps']/df['price']

##### Scoring Criteria
df['a_e/p_rank']=(df['a_e/p'].astype(float)-df['a_e/p'].astype(float).mean())/df['a_e/p'].astype(float).std(numeric_only=False)
df['ret/p_rank']=(df['ret/p'].astype(float)-df['ret/p'].astype(float).mean())/df['ret/p'].astype(float).std(numeric_only=False)
df['divyield_rank']=(df['divyield'].astype(float)-df['divyield'].astype(float).mean())/df['divyield'].astype(float).std(numeric_only=False)

df['yrlow_distance']=(df['price'].astype(float)-df['yrlow'].astype(float))/df['yrlow'].astype(float)
df['yrlow_rank']=(df['yrlow_distance'].astype(float)-df['yrlow_distance'].astype(float).mean())/df['yrlow_distance'].astype(float).std(numeric_only=False)

df['yrhigh_distance']=(df['price'].astype(float)-df['yrhigh'].astype(float))/df['yrhigh'].astype(float)
df['yrhigh_rank']=(df['yrhigh_distance'].astype(float)-df['yrhigh_distance'].astype(float).mean())/df['yrhigh_distance'].astype(float).std(numeric_only=False)

df['fiveyrlow_distance']=(df['price'].astype(float)-df['fiveyrlow'].astype(float))/df['fiveyrlow'].astype(float)
df['fiveyrlow_rank']=(df['fiveyrlow_distance'].astype(float)-df['fiveyrlow_distance'].astype(float).mean())/df['fiveyrlow_distance'].astype(float).std(numeric_only=False)


##### Calculating Score
df['score']=df['ret/p_rank']+df['a_e/p_rank']+df['divyield_rank']-df['yrlow_rank']-df['yrhigh_rank']-df['fiveyrlow_rank']

#### Creating Display
df2=df[['ticker','price','target','a_eps','returns','divyield','score','date','report','note','yrlow','yrhigh','fiveyrlow']].sort_values(by="score", ascending=True)

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 85)

criteria=df2['a_eps']>0
df3=df2[criteria]
print(df3.sort_values(by="score", ascending=False).head(30))
