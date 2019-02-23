'''
########################################################
##         FEDERAL UNIVERSITY OF MINAS GERAIS         ##
##             COMPUTER SCIENCE DEPARTMENT            ##
##             WIRELESS NETWORKS LABORATORY           ##
##                                                    ##
##           Author: Caio Felipe Zanatelli            ##
##                   Fábio Alves Pereira              ##
##                   Marcos Magno de Carvalho         ##
##                                                    ##
########################################################
'''
import numpy as np
from sklearn import datasets
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVR
from sklearn.datasets import make_regression
from sklearn.svm import NuSVR
from sklearn.metrics import mean_squared_error
from math import sqrt

import matplotlib.pyplot as plt

REG_ALGORITHMS = ['nnet', 'lsvr', 'svr', 'nusvr', 'dt', 'gbrt', 'knn', 'rfr']

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
        X = np.loadtxt(self.__dbpath, delimiter=',', usecols=np.arange(0, self.__features),
                    skiprows=1, dtype=float)
        y = np.loadtxt(self.__dbpath, delimiter=',', usecols=(-1), skiprows=1, dtype=float)

        X_test, y_test = None, None

        '''
            TODO: Validate arguments values for each methods. 
        '''
        if self.__algorithm == 'nnet':   # Neural Network Regression
            self.__model = MLPRegressor(
                solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        elif self.__algorithm == 'lsvr': # Linear SVR
            self.__model = LinearSVR(random_state=0, tol=1e-5)
            X, y = make_regression(n_features=self.__features,random_state=0)
        elif self.__algorithm == 'svr':  # SVR
            self.__model = SVR(gamma=1e-5, C=1.0, epsilon=0.2)
        elif self.__algorithm == 'nusvr': # NuSVR
            self.__model = NuSVR(gamma=1e-5, C=1.0, nu=0.1)
        elif self.__algorithm == 'dt':   # Decision Tree
            self.__model = DecisionTreeRegressor(
                min_samples_split=3, random_state=0, max_depth=6)
        elif self.__algorithm == 'gbrt': # Gradient Boosted Regression Trees
            self.__model = GradientBoostingRegressor(
                n_estimators =  500, learning_rate = 0.01, loss = 'ls')
        elif self.__algorithm == 'knn':  # K-Nearest Neighbors Regression
            self.__model = KNeighborsRegressor(n_neighbors = 5)
        elif self.__algorithm == 'rfr':
            self.__model = RandomForestRegressor(
                n_estimators=100, criterion='mse', max_features='sqrt')
        else:
            print('Error. Algorithm not available.')
            sys.exit(1)

        #Case - Uses cross validation, change the variables to fit.
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=90, shuffle=True)

        self.__model.fit(X_train, y_train)
        #print(self.__model.feature_importances_)

        # Root mean square error
        rms = sqrt(mean_squared_error(y_test, self.__model.predict(X_test)))
        #print(rms)
        return rms
        #return X, X_test, y, y_test

    def predict(self, xarray):
        if not self.__model:
            print('Error. Algorithm not set.')
            sys.exit(1)
        else:
            return self.__model.predict(xarray)[0]

    @property
    def features(self):
        return self.__features

    @property
    def algorithm(self):
        return self.__algorithm

    @property
    def dbpath(self):
        return self.__dbpath
