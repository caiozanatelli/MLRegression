#!/usr/bin/env python3.6
import argparse
import numpy as np
import csv
from regression import Regression
from regression import REG_ALGORITHMS

if __name__ == '__main__':
    database = '../tests/exp3.1/ufmg/final.csv'
    
    # Find NuSVR parameters
    #gama, C, epsilon = (0.0, 0.0, 0.0)
    #best_gama, best_C, best_epsilon = (0.0, 0.0, 0.0)
    #best_rms = 9999999.0
    #while gama < 1.0:
    #    print('gama: ', gama)
    #    while C < 2.0:
    #        print('C: ', C)
    #        while epsilon < 2.0:
    #            print('epsilon: ', epsilon)
    #            regression = Regression(database, 'nusvr', 10)
    #            rms = regression.fit()
    #            if rms < best_rms:
    #                best_rms = rms
    #                best_gama = gama
    #                best_C = C
    #                best_epsilon = epsilon
    #            print('Best error so far: ', best_rms)
    #            epsilon += 0.001
    #        C += 0.001
    #    gama += 0.001

    #best_x = 1
    #best_y = 1
    #best_state = 0
    #best_rms = 9999999.0
    #for x in range(1, 20):
    #    for y in range(1, 20):
    #        for state in range(1, 20):
    #            print('x, y, state: ', x, y, state)
    #            regression = Regression(database, 'nnet', 10)
    #            rms = regression.fit((x, y), state)
    #            print('rms: ', rms)
    #            print('')
    #            if rms < best_rms:
    #                best_rms = rms
    #                best_x = x
    #                best_y = y
    #                best_state = state
    
    #print('Best RMS: %f' % (best_rms))
    #print('hidden_layer_sizes=(%d, %d)' % (best_x, best_y))
    #print('random_state=%d' % (best_state))
    #print('gama:    ', best_gama)
    #print('C:       ', best_C)
    #print('epsilon: ', best_epsilon)

    best_est = 0
    best_rms = 9999999.0
    for est in range(1, 2000):
        regression = Regression(database, 'rfr', 10)
        rms = regression.fit(est)
        if rms < best_rms:
            best_rms = rms
            best_est = est

        print('estimators: ', est)
        print('RMS: ', rms)
        print('')
    
    print('Best estimator: ', best_est)
    print('Best RMS: ', best_rms)
    
