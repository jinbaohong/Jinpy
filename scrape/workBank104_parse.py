import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import csv
from random import randint

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

urls = pd.read_csv('result_104/urls_104.csv')
outputFile = 'result_104/company104.csv'
failFile = 'result_104/failFile.csv'


for i in range(len(urls)):
    url = urls.loc[i][0]
    print(url)
    try:
        time.sleep(randint(2,6))
        r = requests.get(url, headers=headers)
    except:
        print('Requesting meets some problems...')
        continue
    soup = BeautifulSoup(r.text, 'html.parser')
    articles = soup.findAll('article')
    for article in articles:
        try:
            tmpList = [article.find('a').text,
                       article.findAll('p')[0].text,
                       article.findAll('p')[1].text,
                       article.findAll('p')[2].text,
                       url]
            with open(outputFile, "a") as fp:
                wr = csv.writer(fp, dialect='excel', quotechar = '"')
                wr.writerow(tmpList)
        except:
            print('There might be some exceptions in this url...')
            with open(failFile, "a") as fp:
                wr = csv.writer(fp, dialect='excel', quotechar = '"')
                wr.writerow([url])
    print('Successful!')

