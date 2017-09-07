from trainNtest import trainNtest
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import Imputer
from sklearn.model_selection import KFold
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier


class dataNtarget(object):
    '''
    Split data into two parts: X and y
     data : pandas.DataFrame
    yName : string
    '''
    def __init__(self, data, yName):
        self.data = data
        self.y = data[yName]
        self.X = data.loc[:,self.data.columns != yName]


def rmCol(pandsDF, colnamesList):
    '''
    remove columns you don't want
        pandasDF : pandas.DataFrame
    colnamesList : list
    return dataframe without columns you don't want.
    '''
    tmp = pandsDF.loc[:,list(map(lambda x: x not in colnamesList,
                       pandsDF.columns))]
    return tmp

def getSplitingData(X, y, splitGenerator):
    '''
                 X : pandas.DataFrame : Data without Y
                 y : pandas.Series    : Data of Y
    splitGenerator : generator        : generator which generate spliting index
    This function fetches only one set of splitting generator.
    So you can get different set whenever you call this function.
    '''
    train_index, test_index = next(splitGenerator)
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    return (X_train, X_test, y_train, y_test)




if __name__ == '__main__':
    titanic = pd.read_csv('titanic/train.csv')
    titanic = rmCol(titanic, ['PassengerId','Name','Ticket','Cabin'])
    titanic = pd.get_dummies(titanic)
    titanic = dataNtarget(titanic, 'Survived')

    kf = KFold( n_splits=10, shuffle=True).split( titanic.X )
    n_splits = 10
    cumulatedTestAccuray = 0
    cumulatedTrainAccuray = 0
    count = 1
    
    while count <= n_splits:
        X_train, X_test, y_train, y_test = getSplitingData(titanic.X, titanic.y, kf)
        imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
        imp = imp.fit(X_train)
        # pd.DataFrame(imp.transform(train_X))
        estimator = GradientBoostingClassifier()
        estimator.fit(imp.transform(X_train), y_train)
        testPredict = pd.Series( estimator.predict( imp.transform( X_test ) ),
                           index = ( y_test.index ) )
        trainPredict = pd.Series( estimator.predict( imp.transform( X_train ) ),
                           index = ( y_train.index ) )

        testAccuracy = sum( testPredict == y_test ) / len(y_test)
        trainAccuracy = sum( trainPredict == y_train ) / len(y_train)
        print( "Round %d ::\ntest accuracy : %f\ntrain accuracy : %f" % (count, testAccuracy, trainAccuracy) )
#         print(confusion_matrix(y_test, testPredict))
        cumulatedTestAccuray = cumulatedTestAccuray + testAccuracy
        cumulatedTrainAccuray = cumulatedTrainAccuray + trainAccuracy
        print("Average test accuray : %f\nAverage train accuracy : %f" % (cumulatedTestAccuray/count, cumulatedTrainAccuray/count))
        count = count + 1







