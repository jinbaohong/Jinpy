import requests
from bs4 import BeautifulSoup

payload = {
    'select_type': 'by Company Name',
    'search_word': '公司'
}

first_page = 1
last_page = 270


for page in range(first_page, last_page+1):
    url = 'http://www.tami.org.tw/category/product4.php?on={}'.format(page)
    print(url)
    
    res = requests.post(url, data=payload)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    for nameTag in soup.select('td.company-word3'):
        with open("mlu.txt", "a") as text_file:
            text_file.write( nameTag.text + '\n' )

