#!/usr/bin/python3.6
from regression import Regression
from regression import REG_ALGORITHMS
import csv
import numpy as np
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Machine Learning Regression Module')
    parser.add_argument('-i', '--input', action='store', type=str, required=True,
                        help='CSV input database path')
    parser.add_argument('-a', '--algorithm', action='store', type=str,
                        choices=REG_ALGORITHMS, default='nnet',
                        help='Regression algorithm to be used for prediction')
    parser.add_argument('-f', '--features', action='store', type=int, default=10,
                        help='Number of features in the database')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    # Build model
    regression = Regression(args.input, args.algorithm, args.features)
    # Train model
    regression.fit(True)
    # Predict output
    print(regression.predict([[10.1,1214873.28,4.0,5.3,3923419136.0,4142837760.0,200138752.0,0.0,0.0,1080.0]]))
