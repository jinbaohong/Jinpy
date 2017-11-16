import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

sleepTime = float(sys.argv[3])
tolerance = int(sys.argv[2])
page = int(sys.argv[1])
failAccrue = 0

while True:
    page = page + 1
    print('p_id = %d ; failAccrue = %d' % (page, failAccrue))
    url = 'http://www.sports.org.tw/c/product/p_viwe.asp?p_id=' + str(page)
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        content = soup.find('body').findAll('table')[3].findAll('tr')[1].text.strip()
        failAccrue = 0
    except (AttributeError, IndexError) as e:
        print('except:', e)
        failAccrue = failAccrue + 1
        if failAccrue > tolerance:
            break
        continue
    with open("soliTmp.csv", "a") as text_file:
        text_file.write( content + '\n' )
    time.sleep(sleepTime)

