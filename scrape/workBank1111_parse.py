import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import csv
from random import randint
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def getValueByKey(soup, key):
    '''
    soup : soup of https://www.1111.com.tw/corp/8525505/
    key : string (regex is available)
    '''
    capitalKey = soup.find('div', text = re.compile(key), attrs = {'class', 'listTitle'})
    if capitalKey != None:
        capitalValue = capitalKey.find_next_sibling("div")
        if capitalValue != None:
            return capitalValue.text
        return 'ValueError'
    return 'KeyError'

def getCompanyName(soup):
    title = soup.find('div', {'class': 'mutitle'})
    try:
        title = title.text
    except:
        title = 'NameError'
    return title

def setDict(soup, dataDict):
    dataDict['公司'] = getCompanyName(soup)
    dataDict['聯絡地址'] = getValueByKey(soup, '聯絡地址')
    dataDict['行業別'] = getValueByKey(soup, '行業別')
    dataDict['統一編號'] = getValueByKey(soup, '統一編號')
    dataDict['資本額'] = getValueByKey(soup, '資本額')
    dataDict['員工人數'] = getValueByKey(soup, '員工人數')
    dataDict['公司電話'] = getValueByKey(soup, '公司電話')
    dataDict['網站位址'] = getValueByKey(soup, '網站位址')
    return dataDict


urls = pd.read_csv('result_1111/urls_1111.csv')
outputFile = 'result_1111/company1111.csv'
failFile = 'result_1111/failFile.csv'

for i in range(len(urls)):
    url = 'https:' + urls.loc[i][0]
    print(url)
    try:
        time.sleep(randint(2,6))
        r = requests.get(url, headers=headers)
    except:
        print('Requesting meets some problems...')
        continue
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        dataDict = dict()
        dataDict = setDict(soup, dataDict)
        temp = pd.DataFrame([dataDict])
        with open(outputFile, 'a') as f:
            temp.to_csv(f, index=False, header=False)
        print('Successful!')
    except:
        print('There might be some exceptions in this url...')
        with open(failFile, "a") as fp:
            wr = csv.writer(fp, dialect='excel', quotechar = '"')
            wr.writerow([url])


