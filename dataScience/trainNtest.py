import numpy as np
import pandas as pd


class trainNtest(object):
    '''
       pandasDF : pandas dataframe : 
              Y : string           :
    testPortion : float            :
    '''
    def __init__(self, pandasDF, Y, testPortion):
        self.pandasDF = pandasDF
        self.Y = Y
        self.sampling = np.random.permutation(len(pandasDF))
        self.testSize = int(testPortion * len(pandasDF))
    def train_X(self):
        train_X = self.pandasDF.iloc[self.sampling[:-self.testSize],self.pandasDF.columns != self.Y]
        return train_X
    def train_y(self):
        train_y = self.pandasDF.loc[self.sampling[:-self.testSize],self.Y]
        return train_y
    def test_X(self):
        test_X = self.pandasDF.iloc[self.sampling[-self.testSize:],self.pandasDF.columns != self.Y]
        return test_X
    def test_y(self):
        test_y = self.pandasDF.loc[self.sampling[-self.testSize:],self.Y]
        return test_y


if __name__ == '__main__':
    iris = pd.read_csv("iris.csv")
    np.random.seed(0)
    x = trainNtest(iris, 'Species', .1)
    print(x.Y, x.testSize)
    print(x.train_X().head())
    print(x.train_y().head())
    print(len(x.train_X()))
    print(x.test_X().head())
    print(x.test_y().head())
    print(len(x.test_X()))

