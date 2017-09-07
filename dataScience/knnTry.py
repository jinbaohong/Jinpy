from trainNtest import trainNtest
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

iris = pd.read_csv('iris.csv')
iris = trainNtest(iris, 'Species', 0.2)

knn = KNeighborsClassifier()
knn.fit(iris.train_X(), iris.train_y())
Ypred = pd.Series(knn.Ypred(iris.test_X()),
                   index = iris.test_y().index)
print(sum( Ypred == iris.test_y() ) / len(iris.test_y()))
print(confusion_matrix(iris.test_y(), Ypred, labels = Ypred.unique()))

