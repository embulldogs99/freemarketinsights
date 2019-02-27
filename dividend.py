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
import numpy as np
import matplotlib.pyplot as plt
import datetime


def div():
    with requests.Session() as c:
        u="https://www.dividendchannel.com/history/?symbol=MSFT"
        x=c.get(u)
        x=BeautifulSoup(x.content, "html.parser")
        t=x.find_all('script')
        for z in t:
            print(z)
div()
