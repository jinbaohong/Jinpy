import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def getPageTotal(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        pageString = soup.find("div", {"class": "page-total"}).text
        pageTotal = [int(s) for s in pageString.split() if s.isdigit()][0]
        return pageTotal
    except:
        print('Fail when getting page-total...')
        return 1

# url = 'https://www.104.com.tw/cust/list/index/?page=1&order=1&emp=8&cpt=8&mode=s&jobsource=checkc'
# pageTotal = getPageTotal(url)

sleepTime = 3
combinations = list()
url_render = 'https://www.104.com.tw/cust/list/index/?page={}&order=1&emp={}&cpt={}&mode=s&jobsource=checkc'
for emp in range(1,9):
    for cpt in range(1,9):
        time.sleep(sleepTime)
        print('Combination emp={}, cpt={}'.format(emp, cpt))
        # Get total-page number from first page of each combination
        url_combination = url_render.format(1, emp, cpt)
        pageTotal = getPageTotal(url_combination)
        # Put all the urls of a specific combination into a list
        combinations.append([url_render.format(i + 1, emp, cpt) for i in range(pageTotal)])

df = pd.Series(combinations[0])
for i in range(1,len(combinations)):
    df = df.append(pd.Series(combinations[i]))
df.to_csv('result_104/urls_104.csv', index=False)


