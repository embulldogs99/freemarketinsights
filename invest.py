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
from decimal import *



def portfolioinvestmentadder(amount):
    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("""SELECT date,portfolio FROM fmi.portfoliohistory ORDER BY date asc;""")
    portfolio=cur.fetchall()
    for d,p in portfolio:
        newportvalue=float(p)+amount
        cur.execute("""UPDATE fmi.portfoliohistory set portfolio=%s WHERE date=%s;""", (newportvalue,d))
        conn.commit()
    cur.close()
    conn.close()

amount=input("Input Cash Increase Amount: ")
portfolioinvestmentadder(float(amount))


def stockbuy(ticker,shares,price,target_price):
    ticker=str(ticker)
    shares=int(shares)
    price=float(price)
    target_price=int(target_price)
    value=round(shares*price,2)
    exp_return=round((target_price-price)/price,2)
    exp_value=round(shares*price*exp_return,2)


    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()


    cur.execute("""SELECT value FROM fmi.portfolio where ticker='CASH';""")
    cash=cur.fetchall()
    for c in cash:
        newcash=float(c[0])-value
    cur.execute("""UPDATE fmi.portfolio set shares=%s,value=%s,exp_value=%s WHERE ticker=%s;""", (newcash,newcash,newcash,'CASH'))
    conn.commit()

    cur.execute("""INSERT INTO fmi.portfolio (ticker, shares, price, value, target_price,exp_return,exp_value) VALUES (%s,%s,%s,%s,%s,%s,%s);""", (ticker,shares,price,value,target_price,exp_return,exp_value))
    conn.commit()

    cur.close()
    conn.close()



def stocksell(ticker,shares,price):
    ticker=str(ticker)
    shares=int(shares)
    price=float(price)
    value=round(shares*price,2)

    conn = psycopg2.connect("dbname='postgres' user='postgres' password='postgres' host='localhost' port='5432'")
    cur = conn.cursor()


    cur.execute("""SELECT value FROM fmi.portfolio where ticker='CASH';""")
    cash=cur.fetchall()
    for c in cash:
        newcash=float(c[0])+value

    cur.execute("""UPDATE fmi.portfolio set shares=%s,value=%s,exp_value=%s WHERE ticker=%s;""", (newcash,newcash,newcash,'CASH'))
    conn.commit()

    stmt="DELETE FROM fmi.portfolio where ticker="+ticker
    cur.execute(stmt)
    conn.commit()

    cur.close()
    conn.close()



buysell=input("Buying Stock: type 1. Selling stock: type 2.: ")
try:
    buysell=int(buysell)
except:
    print("You did not select a valid option")

if buysell==1:
    ticker=input("What stock ticker are you buying?: ")
    shares=input("How many shares?: ")
    price=input("For what stock price?: ")
    target_price=input("What is your target price?: ")
    stockbuy(ticker,shares,price,target_price)

if buysell==2:
    ticker=input("What stock ticker are you selling?: ")
    shares=input("How many shares?: ")
    price=input("For what stock price?: ")
    stocksell(ticker,shares,price)



import portfoliohistoryupdate
