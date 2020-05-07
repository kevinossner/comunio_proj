#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 19:10:43 2020

@author: kevinossner
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import pandas as pd

url = 'https://stats.comunio.de/squad'

uClient = urlopen(url)
page_html = uClient.read()
uClient.close()

# parse html
page_soup = soup(page_html, 'html.parser')

clubs = page_soup.find('td', {'class':'clubPics'})

urls = []
for link in clubs.findAll('a'):
    x = link.get('href')
    x = x.replace("ä","ae").replace("ö","oe").replace("ü","ue")
    x = 'https://stats.comunio.de' + x
    urls.append(x)

df = pd.DataFrame([])

for url in urls:

    uClient = urlopen(url)
    page_html = uClient.read()
    uClient.close()

    # parse html
    page_soup = soup(page_html, 'html.parser')

    tables = page_soup.findAll('table', {'class':'rangliste playersTable autoColor tablesorter zoomable'})

    table = tables[0].tbody



    trs = table.find_all("tr")

    team = pd.DataFrame([])

    for i in range(1, len(trs)-1, 1):
        if len(trs[i].get_text()) > 0:
            index = range(0, 1, 1)
            columns = ['name', 'position', 'points', 'market_value']
            player = pd.DataFrame(index=index, columns=columns)
            values = list(filter(None, trs[i].get_text().split('\n')))
            player['name'] = values[0]
            player['position'] = values[1]
            player['points'] = values[2]
            player['market_value'] = values[3]
            player['club'] = url.split('-')[1]
            team = team.append(player)
        

    df = df.append(team)

df['club'] = df['club'].apply(lambda x: x.replace('+', ' '))
df['market_value'] = df['market_value'].apply(lambda x: x.replace('.', ''))
df['market_value'] = df['market_value'].astype(float)
df['points'] = df['points'].astype(float)
df.to_csv('./data/comunio.csv', index=False)