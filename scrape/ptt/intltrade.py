#!/usr/bin/env python3

from random import randint
import time
import requests
from bs4 import BeautifulSoup
import bs4
from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
              'Referer': 'https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do'}

def getMainContent(mainDiv):
    contentList = []
    tmpContent = ''
    for tag in mainDiv:
        if (type(tag) is bs4.element.NavigableString):
            tmpContent += tag
            continue
        if tag['class'][0] == 'f6':
            tmpContent += tag.text
        if tag['class'][0] == 'f2':
            tmpContent += tag.text
        if tag['class'][0] == 'push':
            if tmpContent: contentList.append({'type': 'main',
                                               'content': tmpContent})
            tmpContent = ''
            contentList.append({'type': 'push',
                                'content': {
                                    'pushTag': tag.findAll('span')[0].text,
                                    'pushUserid': tag.findAll('span')[1].text,
                                    'pushContent': tag.findAll('span')[2].text,
                                    'pushIpDateTime': tag.findAll('span')[3].text}
                               })
    if tmpContent: contentList.append({'type': 'main',
                                       'content': tmpContent})
    return contentList

def setDict(soup, url):
    result = dict()
    mainDiv = soup.find('div', {'id':'main-content'})
    metaInfos = mainDiv.findAll('div', {'class':'article-metaline'})
    result['author'] = metaInfos[0].findAll('span')[1].text
    result['title'] = metaInfos[1].findAll('span')[1].text
    result['timeStamp'] = metaInfos[2].findAll('span')[1].text
    result['mainContent'] = getMainContent(mainDiv)
    result['length'] = len(result['mainContent'])
    result['uri'] = url
    return result

uri = 'mongodb://172.20.23.138:27017'
client = MongoClient(uri)
db = client['ptt']
collect = db['intltrade']

count = 0
failFile = 'failUrls.text'
with open("urls.txt", encoding="utf-8") as file:
    urls = [l.strip() for l in file]

for url in urls:
    count += 1
    print('%2f' % (count/13315))
    time.sleep(randint(2,6))
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        collect.insert_one(setDict(soup, url))
    except:
        with open(failFile, "a") as text_file:
            text_file.write(url + '\n')

