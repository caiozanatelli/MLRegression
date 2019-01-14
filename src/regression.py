import numpy as np
from sklearn import datasets
from sklearn import svm
from svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

REG_ALGORITHMS = ['nnet', 'svr', 'dt', 'gbrt', 'knn']

class Regression:
    '''
    Regression Module implementing selected Machine Learning algorithms.

    TODO: add cross-validation and plot errors for algorithsm comparison (IMPORTANT)
    '''

    def __init__(self, dbpath, algorithm, nfeatures):
        self.__features = nfeatures
        self.__algorithm = algorithm
        self.__dbpath = dbpath
        self.__model = None

    def fit(self):
        X = np.loadtxt(self.__dbpath, delimiter=',', usecols=np.arange(0, self.__features), skiprows=1)
        y = np.loadtxt(self.__dbpath, delimiter=',', usecols=(-1), skiprows=1)

        if self.__algorithm == 'nnet':   # Neural Network Regression
            self.__model = MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        elif self.__algorithm == 'svr':  # SVR
            self.__model = SVR(gamma='scale', C=1.0, epsilon=0.2)
        elif self.__algorithm == 'dt':   # Decision Tree
            pass
        elif self.__algorithm == 'gbrt': # Gradient Boosted Regression Trees
            pass
        elif self.__algorithm == 'knn':  # K-Nearest Neighbors Regression
            pass
        else:
            print('Error. Algorithm not available.')
            sys.exit(1)

        self.__model.fit(X, y)

    def predict(self, xarray):
        if not self.__model:
            print('Error. Algorithm not set.')
            sys.exit(1)
        else:
            return self.__model.predict(xarray)

    @property
    def features(self):
        return self.__features

    @property
    def algorithm(self):
        return self.__algorithm

    @property
    def dbpath(self):
        return self.__dbpath
