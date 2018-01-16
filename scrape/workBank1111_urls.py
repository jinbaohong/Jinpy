import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import csv
from random import randint
import re


def getHrefFromDigest(digest):
    try:
        cpyinfo = digest.find('div', {'class': 'cpyinfo'})
        link = cpyinfo.find('a')['href']
    except:
        link = 'FailLink'
    return link


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url_render = 'https://www.1111.com.tw/job-bank/job-index.asp?si=2&fs=0&pt=0&ps=100&page={}'
sleepTimeMax = 5

for page in range(1, 61):
    url = url_render.format(page)
    time.sleep( randint(1, sleepTimeMax) )
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    digests = soup.findAll("li", {"class": "digest "})
    print(url)
    for digest in digests:
        content = getHrefFromDigest(digest)
        with open("result_1111/urls_1111.csv", "a") as text_file:
            text_file.write( content + '\n' )



