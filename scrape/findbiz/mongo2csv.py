#!/usr/bin/env python3

from pymongo import MongoClient
import pandas as pd

uri = 'mongodb://172.20.23.138:27017'
client = MongoClient(uri)

db = client['findbiz']
collect = db['companies']

query1 = collect.find({})
tmp = query1.next()

DF = pd.DataFrame([list(tmp.values())], columns=list(tmp.keys()))
while True:
    try:
        print(DF.shape[0])
        tmp = query1.next()
        tmpDF = pd.DataFrame([list(tmp.values())], columns=list(tmp.keys()))
        DF = DF.append(tmpDF)
    except:
        print('finish!')

DF.to_csv('mongo2csv.csv',index=False)
