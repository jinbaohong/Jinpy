from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def getMatchByTfidf(corpus, query):
    tfidf = TfidfVectorizer()
    tfs = tfidf.fit_transform(corpus)

    response = tfidf.transform([query])
#     feature_names = tfidf.get_feature_names()
#     for col in response.nonzero()[1]:
#         print( feature_names[col], ' - ', response[0, col])
#     print(np.amax(np.sum(tfs.toarray()[:,response.nonzero()[1]], axis=1)))
#     print(tfs.toarray()[:,response.nonzero()[1]])
    # Print the highest tfidf score
    print(np.amax(np.sum(tfs.toarray()[:,response.nonzero()[1]], axis=1)))
    # best : the location in corpus of the best score
    best = np.argmax(np.sum(tfs.toarray()[:,response.nonzero()[1]], axis=1))
    if best:
        # if best score is not zero, then return the corpus
        return corpus[best]
    return 'Exception: No matching'

if __name__ == '__main__':
    text1 = 'Cosmoprof North America Las Vegas(Cosmoprof)'
    text2 = 'National Safety Council Congress & Expo Anaheim 2016(NSC Congress & Expo)'
    text3 = 'NSC - National Safety Council Congress & Exposition'
    text5 = 'International Consumer Electronics Show(2013 International CES)'

    query = 'congress International CES - Consumer Electronics Show - the Source for Consumer Technologies'
    query2 = 'safety    2016'
    query3 = ''
    query4 = 'you are a ass hole congress'

    corpus = (text1, text2, text3, text5)

    print(getMatchByTfidf(corpus, query2))
    print(getMatchByTfidf(corpus, query3))
    print(getMatchByTfidf(corpus, query))
    print(getMatchByTfidf(corpus, query4))

