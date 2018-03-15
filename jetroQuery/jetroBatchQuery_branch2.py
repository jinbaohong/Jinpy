from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
import csv
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer  
import sys
from multiprocessing.dummy import Pool as ThreadPool
import time


def containTerm(term, mainResult):
    mainResult = cleanWords(mainResult)
    return term in mainResult

# mainResult = 'MAGICONLINE veryRareWord- PROJECT'
# containTerm('magica', mainResult)



def get_hitw(tfidf, query, order):
    # hitw : high informative term weight
    unigrams = query.split(' ')
    dataDict = dict()
    for i in range(len(unigrams)):
        loc0 = tfidf.vocabulary_.get(unigrams[i])
        if loc0 == None:
            continue
        dataDict[unigrams[i]] = tfidf.idf_[loc0]
    s = [(k, dataDict[k]) for k in sorted(dataDict, key=dataDict.get, reverse=True)]
    # tw_tup : term-weight tuple
    if len(s) == 0:
        return ('NoWord', 0.0)
    if order > len(s):
        order = len(s)
    tw_tup = s[order - 1]
    return tw_tup

# query = 'MAGICONLINE veryRareWord- PROJECT'
# query = cleanWords(query)
# get_hitw(tfidf, query, 3)


def cleanWords(query):
    try:
        # Get tokens
        counterTemp = CountVectorizer(ngram_range=(1,1))
        langModTemp = counterTemp.fit_transform([query])
        unigrams = counterTemp.get_feature_names()
        # Remove stopwords
        filtered_words = [word for word in unigrams if word not in stopwords.words('english')]
        # Lemmatize or stemming
        # This could be altered by st.stem(word)
        # or
        # snowball_stemmer = SnowballStemmer('english')  
        # snowball_stemmer.stem(word)
        wnl = WordNetLemmatizer()
        cleanWords = [wnl.lemmatize(word, "v") for word in filtered_words]
        # Concatenate
        sentence = ' '.join(cleanWords)
    except ValueError:
        print('perhaps the documents only contain stop words')
        return ' '
    return sentence

# text4 = 'congress International CES - Consumer Electronics Show - the Source for Consumer Technologies'
# cleanWords(text4)



def matchEngine(tfidf, tfs, query):
    queryCleaned = cleanWords(query)
    response = tfidf.transform([queryCleaned])
    score = np.amax(np.sum(tfs.toarray()[:,response.nonzero()[1]], axis=1))
    score_std = score / len(response.nonzero()[1])
    best = np.argmax(np.sum(tfs.toarray()[:,response.nonzero()[1]], axis=1))
    matchResult = my_data.loc[best][1]
    hitw_tup1 = get_hitw(tfidf, queryCleaned, 1)
    hitw_tup2 = get_hitw(tfidf, queryCleaned, 2)
    hitw1 = hitw_tup1[1]
    hitw2 = hitw_tup2[1]
    hit1 = hitw_tup1[0]
    hit2 = hitw_tup2[0]
    contain_hit1 = containTerm(hit1, matchResult)
    contain_hit2 = containTerm(hit2, matchResult)
    
    tmpList = [query,
               matchResult,
               int(my_data.loc[best][0]),
               score,
               score_std,
               hit1,
               hitw1,
               contain_hit1,
               hit2,
               hitw2,
               contain_hit2]
    return tmpList


# tfidf = TfidfVectorizer()
# tfs = tfidf.fit_transform(corpusProcessed)
# query = 'MAGICONLINE veryRareWord- PROJECT'
# query = cleanWords(query)
# matchEngine(tfidf, tfs, query)




# exhibitMainFile = 'data/exhibitMain0108.csv'
# queryFile = 'data/Jetro0108_1_.csv'
# outputFile = 'output/output0108_1_.csv'

exhibitMainFile = str(sys.argv[1])
queryFile = str(sys.argv[2])
outputFile = str(sys.argv[3])

#if os.path.isfile(outputFile):
    


queryTable = pd.read_csv(queryFile)
my_data = pd.read_csv(exhibitMainFile, encoding = "ISO-8859-1")
corpusOriginal = tuple(my_data['text'])
print('Cleaning corpus...')
# corpusProcessed = map(cleanWords, corpusOriginal)
corpusProcessed = [cleanWords(x) for x in corpusOriginal]

print('Vectorizing...')
tfidf = TfidfVectorizer()
tfs = tfidf.fit_transform(corpusProcessed)

with open(outputFile, "w") as fp:
    wr = csv.writer(fp, dialect='excel', quotechar = '"')
    wr.writerow(['dataId',
                 'query',
                 'matchResult',
                 'showId',
                 'Score',
                 'ScoreStd',
                 'hit1',
                 'hitw1',
                 'contain_hit1',
                 'hit2',
                 'hitw2',
                 'contain_hit2'])
def writeMatch(index):
    print('Querying %d...' % index)
    dataId = queryTable.loc[index]['dataId']
    query = queryTable.loc[index]['query']
    tmpList = matchEngine(tfidf, tfs, query)
    tmpList = [dataId] + tmpList
    with open(outputFile, "a") as fp:
        wr = csv.writer(fp, dialect='excel', quotechar = '"')
        wr.writerow(tmpList)
start_time = time.time()
pool = ThreadPool(4)
pool.map(writeMatch, range(len(queryTable)))
pool.close()
pool.join()
print("--- %s seconds ---" % (time.time() - start_time))




