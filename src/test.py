#!/usr/bin/env python3.6
import argparse
import numpy as np
import csv
from regression import Regression
from regression import REG_ALGORITHMS

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Regression Module Test Suite')
    parser.add_argument('-i', '--input', action='store', type=str, required=True,
                        help='CSV input database path')
    parser.add_argument('-a', '--algorithm', action='store', type=str,
                        choices=REG_ALGORITHMS, default='nnet',
                        help='Regression algorithm to be used for prediction')
    parser.add_argument('-f', '--features', action='store', type=int, default=10,
                        help='Number of features in the database')
    args = parser.parse_args()

    # Build model
    regression = Regression(args.input, args.algorithm, args.features)
    rms = regression.fit()
    print(rms)

