import json
import pandas as pd

data = json.load(open('vdinfo.json'))

listOfRawData = data.get('XML_Head').get('Infos').get('Info')
listOfRawData[0]
pd.DataFrame([listOfRawData[0]])

