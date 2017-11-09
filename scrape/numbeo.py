
# coding: utf-8

# In[24]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.numbeo.com/pollution/rankings_by_country.jsp'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(url, headers=headers)


soup = BeautifulSoup(r.text, 'html.parser')

rows = soup.tbody.findAll('tr')
with open("tmp.csv", "a") as text_file:
    text_file.write( 'Country,PollutionIndex,ExpPollutionIndex' + '\n' )
for row in rows:
    parts = row.findAll('td')
    tmp = []
    for i in range(1,4):
        tmp.append(parts[i].text)
    tmp = ','.join( list( map(str, tmp) ) )
    with open("tmp.csv", "a") as text_file:
        text_file.write( tmp + '\n' )


# In[ ]:




