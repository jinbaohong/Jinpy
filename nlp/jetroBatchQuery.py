from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import pandas as pd
import csv



my_data = pd.read_csv('data/exhibitMain1228.csv', encoding = "ISO-8859-1")
corpus = tuple(my_data['text'])
tfidf = TfidfVectorizer(stop_words=None)
print('Vectorizing...')
tfs = tfidf.fit_transform(corpus)

queryTable = pd.read_csv('data/Jetro1227.csv')

outputFile = 'output/output1228_.csv'
with open(outputFile, "a") as fp:
    wr = csv.writer(fp, dialect='excel', quotechar = '"')
    wr.writerow(['dataId', 'query', 'mainText', 'showId', 'Score', 'ScoreStd'])
for index in range(len(queryTable)):
    print('Querying %d...' % index)
    dataId = queryTable.loc[index][0]
    query = queryTable.loc[index][1]
    response = tfidf.transform([query])
    score = np.amax(np.sum(tfs.toarray()[:,response.nonzero()[1]], axis=1))
    score_std = score / len(response.nonzero()[1])
    best = np.argmax(np.sum(tfs.toarray()[:,response.nonzero()[1]], axis=1))
    tmpList = [dataId,
               query,
               my_data.loc[best][1],
               int(my_data.loc[best][0]),
               score,
               score_std]
    with open(outputFile, "a") as fp:
        wr = csv.writer(fp, dialect='excel', quotechar = '"')
        wr.writerow(tmpList)






