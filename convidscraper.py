#!/usr/bin/python

#pip install requests
#pip install bs4
from datetime import datetime, date
import os.path
from os import path

import requests
from bs4 import BeautifulSoup
import csv

dt = datetime.now().strftime("%Y-%m-%d")

URL = "https://dph.georgia.gov/covid-19-daily-status-report"
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html.parser')

data=[]

for caption in soup.find_all('caption'):
    if caption.get_text() == 'COVID-19 Confirmed Cases by County':
        table = caption.find_parent('table', {'class': 'stacked-row-plus'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) # Get rid of empty values
filename = 'georgia_convid19.csv'
noheader=False
if os.path.exists(filename):
	noheader=True
with open(filename, 'ab') as f:
    w = csv.DictWriter(f,['date','county','count']) 
    if noheader != True:
        w.writeheader() 
    for d in data: 
        w.writerow({'date': dt, 'county' : d[0], 'count' : d[1]})
