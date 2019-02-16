import requests
import bs4
from bs4 import BeautifulSoup
import warnings
import time
import datetime
import json
import pandas as pd
import io
import re
import psycopg2
import quandl
import random
import os
import shutil
#
# os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
# shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")


#########################################################
##############  Database Connection   ###################



conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
cur = conn.cursor()

# marketbulls
cur.execute("COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(m))) FROM (SELECT * FROM(SELECT DISTINCT on (ticker) target,price,round(returns*100) as returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield FROM fmi.marketmentions WHERE report='analyst' AND date > current_timestamp - INTERVAL '20 days' ORDER BY ticker,returns DESC) t ORDER BY returns DESC LIMIT 5 ) m)  to 'F:/json/marketbulls.json'")

conn.commit()
print("----------------------------")
print("pulled market bulls")
print("----------------------------")

shutil.move("F:\json\marketbulls.json","dist/json/marketbulls.json")

#MarketBears

cur.execute("COPY (SELECT ARRAY_TO_JSON(ARRAY_AGG(ROW_TO_JSON(m))) FROM (SELECT * FROM(SELECT DISTINCT on (ticker) target,price,round(returns*100) as returns,ticker,note,to_char(date,'MM/DD/YYYY'),q_eps,a_eps,report,q_pe,a_pe,divyield FROM fmi.marketmentions WHERE report='analyst' AND date > current_timestamp - INTERVAL '20 days' ORDER BY ticker,returns ASC) t ORDER BY returns ASC LIMIT 5 ) m)  to 'F:/json/marketbears.json'")
conn.commit()
print("----------------------------")
print("pulled market bears")
print("----------------------------")

shutil.move("F:\json\marketbears.json","dist/json/marketbears.json")


#PortfolioHistory
cur.execute("COPY (SELECT to_char(date,'MM/DD/YYYY'),portfolio,snp,nasdaq,portfolioreturn,snpreturn,nasdaqreturn FROM fmi.portfoliohistory) to 'F:/json/portfoliohistory.json'")
conn.commit()
print("----------------------------")
print("pulled portfoliohistory")
print("----------------------------")
shutil.move("F:\json\portfoliohistory.json","dist/json/portfoliohistory.json")


cur.close()
conn.close()
