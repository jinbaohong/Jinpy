import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

for page in range(1, 3114):
    url = 'http://www.sports.org.tw/c/product/p_viwe.asp?p_id=' + page
    r = requests.get(url, headers=headers)
    r.encoding = 'big5'
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find('body').findAll('table')[3].findAll('tr')[1].text.strip()
    with open("soliTmp.csv", "a") as text_file:
        text_file.write( content + '\n' )
    time.sleep(2)

