import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
from random import randint
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'


def getIndusValue(keySoup):
    #========================
    '''
    keySoup : soup of industry key, i.e. 
    output : Cleaned string of the value soup
    '''
    #========================
    # value soup is the sibling of the key soup.
    try:
        indus_type = keySoup.find_next_sibling('td').text
        # substitute all the \r\n\t
        indus_type = re.sub(r'[\r|\n|\t| |\xa0]', ' ', indus_type)
        # replace the space between digits and chinese
        indus_type = re.sub(r'([0-9])[ ]+([\u4E00-\u9FFF\u3000-\u303F])', r'\1_\2', indus_type)
        # concate all the indust type
        indus_type = re.sub(r'[ ]+', r';', indus_type)
    except:
        return 'indusValueError'
    return indus_type

# getIndusValue(keySoups[9])



def parseElements(keySoups):
    #========================
    '''
    keySoups : soups of all keys, i.e. soup.find('tbody').findAll('td', {'class':'txt_td'})
    output : dict of all soups value
    '''
    #========================
    dataDict = dict()
    for keysoup in keySoups:
        # test if the keysoup has attribute 'text'
        if not hasattr(keysoup, 'text'):
            continue
        if keysoup.text == '所營事業資料':
            # 所營事業資料's value needs getIndusValue() to parse
            value = getIndusValue(keysoup)
            dataDict[keysoup.text] = value
            continue
        if keysoup.text == '公司名稱':
            # 公司名稱'x value needs a special way to parse
            try:
                compName = keysoup.find_next_sibling('td').span['onclick']
                value = re.sub(r'[^\u4E00-\u9FFF\u3000-\u303F]', '', compName)
                dataDict[keysoup.text] = value
            except:
                dataDict[keysoup.text] = 'compNameError'
            continue
        # Most of the value can be parsed by the way following
        try:
            value = keysoup.find_next_sibling('td').find(text=True, recursive=False)
            dataDict[keysoup.text] = re.sub(r'[\r|\n|\t| |\xa0]', '', value)
        except:
            dataDict[keysoup.text] = keysoup.text + 'Error'
    return dataDict

def getDataFromUrl(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
              'Referer': 'https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    keySoups = soup.find('tbody').findAll('td', {'class':'txt_td'})
    return parseElements(keySoups)

# url = 'https://findbiz.nat.gov.tw/fts/query/QueryCmpyDetail/queryCmpyDetail.do?objectId=SEM3MDQ0MDE2Mw==&banNo=70440163'
# url = 'https://findbiz.nat.gov.tw/fts/query/QueryCmpyDetail/queryCmpyDetail.do?objectId=SEMyODY3OTA5Mg==&banNo=28679092'
# url = 'https://findbiz.nat.gov.tw/fts/query/QueryCmpyDetail/queryCmpyDetail.do?objectId=SEM1MjU4MDY5Nw==&banNo=52580697'
# url = 'https://findbiz.nat.gov.tw/fts/query/QueryCmpyDetail/queryCmpyDetail.do?objectId=SEMxNjIxMTQxOQ==&banNo=16211419'


# with open('data.txt', 'w') as outfile:
# json.dumps(getDataFromUrl(url)).decode('unicode-escape').encode('utf8')
def appendJsonInfo(outputFile, url):
    getStringWithDecodedUnicode = lambda str : re.sub( '\\\\u([\da-f]{4})', (lambda x : chr( int( x.group(1), 16 ) )), str )
    jsonString = json.dumps( getDataFromUrl(url) )
    jsonString = getStringWithDecodedUnicode( jsonString )
    with open(outputFile, "a") as text_file:
        text_file.write(',\n"{}":'.format(url))
        text_file.write(jsonString)


# companies = soup.findAll('div', {'class': 'panel panel-default'})
def getCompanyHref(company):
    '''
    company : soup of company
    Example :
    companies = soup.findAll('div', {'class': 'panel panel-default'})
    company = companies[7]
    '''
    try:
        href = company.a['href']
    except:
        return 'urlError'
    href_fix = 'https://findbiz.nat.gov.tw' + re.sub(r'[\r|\n]', '', company.a['href'])
    return href_fix
# getCompanyHref(companies[2])

def getCompanyName(company):
    '''
    company : soup of company
    Example :
    companies = soup.findAll('div', {'class': 'panel panel-default'})
    company = companies[7]
    '''
    try:
        company_name = re.sub(r'[\r|\n|\t| ]', '', company.a.text)
    except:
        return 'companyNameError'
    # company's info: for augment
    # company_info = re.sub(r'[\r|\n|\t| ]', '', company.findAll('div')[1].text)
    return company_name
# getCompanyName(companies[2])


def getPageTotal(soup):
    '''
    soup : request page's soup
    '''
    try:
        totalTab = soup.find('span', {'id': 'lblTopTotal'})
    except:
        print('getPageTotal fail !')
        return 1
    try:
        testString = re.sub(r'[\n|\t|\r|\xa0]', '', totalTab.parent.text)
        pageTotal = re.sub(r'(^.*[分]|[頁].*$|,)', '', testString)
    except:
        print('getPageTotal parsing fail !')
        return 1
    return int(pageTotal)
# getPageTotal(soup)

def setPayload(currentPage, busiItemSub):
    '''
    currentPage: '103'
    busiItemSub: 'C301010'
    '''
    payload = {
        'pagingModel.currentPage':str(currentPage),
        'model.qryCond':'公司',
        'model.isAlive':'true',
        'model.cmpyType':'true',
        'model.infoType':'D',
        'model.busiItemSub':str(busiItemSub)
    }
    return payload
# setPayload(1234, 'asdf')


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
          'Referer': 'https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do'}
url = 'https://findbiz.nat.gov.tw/fts/query/QueryList/queryList.do'

items = pd.read_csv('config/items.csv')
items = items['itemId']
# outputFile = 'urls/url.csv'
outputFile = 'company_findbiz.json'

with open(outputFile, "w") as text_file:
    text_file.write('{')
for item in items:
    # Find pageTotal of every item, say, C301010 has 21 pages.
    print('Iterating item: %s now...' % (item))
    payload = setPayload(1, item)
    time.sleep(randint(2,6))
    try:
        r = requests.post(url, headers=headers, data=payload)
    except:
        print('Request item fail...')
        continue
    soup = BeautifulSoup(r.text, 'html.parser')
    pageTotal = getPageTotal(soup)
    for page in range(1, pageTotal + 1):
        # Request all pages of the item, say, C301010.
        print('Iterating item: %s, page: %d now...' % (item, page))
        payload = setPayload(page, item)
        time.sleep(randint(2,6))
        try:
            r = requests.post(url, headers=headers, data=payload)
        except:
            print('Request page fail...')
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        companies = soup.findAll('div', {'class': 'panel panel-default'})
        for company in companies:
            # Parse all company's href and name from the page.
            # companyName = getCompanyName(company)
            time.sleep(randint(2,6))
            href = getCompanyHref(company)
            # Write information into outputFile
            appendJsonInfo(outputFile, href)
with open(outputFile, "a") as text_file:
    text_file.write('}')

