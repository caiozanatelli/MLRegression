#!/usr/bin/python3.6
########################################################
##         FEDERAL UNIVERSITY OF MINAS GERAIS         ##
##             COMPUTER SCIENCE DEPARTMENT            ##
##             WIRELESS NETWORKS LABORATORY           ##
##                                                    ##
##           Author: Caio Felipe Zanatelli            ##
##                   Marcos Magno de Carvalho         ##
##                                                    ##
########################################################
from regression import Regression
from regression import REG_ALGORITHMS
import csv
import numpy as np
import argparse
import socket
import sys
import select
import configparser
from copa_api import APICopa
from numpy import array
#import Queue
from multiprocessing import Queue

def parse_args():
    parser = argparse.ArgumentParser(description='Machine Learning Regression Module')
    parser.add_argument('--bufmg', action='store', type=str, default='../tests/ufmg_norm.csv',
                        help='CSV input database path for UFMG pool')
    parser.add_argument('--bufrgs', action='store', type=str, default='../tests/ufrgs_norm.csv',
                        help='CSV input database path for UFRGS pool')
    parser.add_argument('-a', '--algorithm', action='store', type=str,
                        choices=REG_ALGORITHMS, default='nnet',
                        help='Regression algorithm to be used for prediction')
    parser.add_argument('-f', '--features', action='store', type=int, default=5,
                        help='Number of features in the database')
    parser.add_argument('-x', action='store', type=float, default=0.5, help='Define the tolerance')
    parser.add_argument('--fps', action='store', type=int, default=30, help='Default fps')

    return parser.parse_args()

def get_locus(conf_file = 'pools.conf'):
    config = configparser.ConfigParser()   

    try:
        config.read(conf_file)
        return config['POOLS']['pool1'], config['POOLS']['pool2']

    except FileExistsError as e:
        print("Warning: Configuration File not found. Using default values")

def is_edge(pool):
    return get_locus()[0] == pool

def is_cloud(pool):
    return get_locus()[1] == pool

def migrate(pools, tolerance_predict):
    #time_edge, time_cloud = pools[get_locus()[0]], pools[get_locus()[1]]
    global pool_locus
    time_edge, time_cloud = 0,0
    try:
        time_edge = pools[get_locus()[0]]
    except KeyError:
        pools[get_locus()[0]] = 999999999

    try:
        time_cloud = pools[get_locus()[1]]
    except KeyError:
        pools[get_locus()[1]] = 999999999

    pool_destination = pool_locus
    if is_edge(pool_locus) and time_edge >= tolerance_predict:
        pool_destination = min(pools, key=pools.get)
    elif is_cloud(pool_locus) and time_cloud < tolerance_predict:
        pool_destination = get_locus()[0]

    if pool_destination != pool_locus:
        print("Pool Locus", pool_locus)
        print("Pool Desti", pool_destination) 
        APICopa().migrateContainer(pool_locus, pool_destination.replace("\'",""))
        pool_locus = pool_destination

if __name__ == '__main__':
    global pool_locus
    pool_locus = get_locus()[1]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(0)
    server_address = ('192.168.0.52', 10001)
    server.bind(server_address)
    server.listen(5)
    inputs = [server]
    outputs = [ ]      
    pools = {}  
    message_queues = {}    
    args = parse_args()
    # Start connection

    # Build model
    model_ufmg = Regression(args.bufmg, args.algorithm, args.features)
    model_ufrgs = Regression(args.bufrgs, args.algorithm, args.features)
    model_ufmg.fit()
    model_ufrgs.fit()
    # Train model
    
    # Predict output

    #server = Server()
    #print(server.handleConnection())

    while inputs:    

        # Wait for at least one of the sockets to be ready for processing
	#print >>sys.stderr, '\nwaiting for the next event'
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        # Handle inputs
        for s in readable:
            if s is server:
                # A "readable" server socket is ready to accept a connection
                connection, client_address = s.accept()
                #print >>sys.stderr, 'new connection from', client_address
                connection.setblocking(0)
                inputs.append(connection)

                # Give the connection a queue for data we want to send
                #message_queues[connection] = Queue.Queue()
            else:
                #data = s.recv(1024)
                data = s.recv(1024).decode('utf-8')
                if data:
                    #print(data)
                    # A readable client socket has data
                    #print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
                    #message_queues[s].put(data)
                    cpu_percentage__ = data.split(',')[0]
                    cpu_percentage = str(cpu_percentage__).split('[')[1]
                    cpu_time = data.split(',')[1]
                    m_available = data.split(',')[2]
                    m_swap = data.split(',')[3]
                    frame_rate = data.split(',')[4]
                    #net_traffic = data.split(',')[4]
                    #transmission_capture = data.split(',')[5]
                    #transmission_observer = data.split(',')[6]                        
                    
                    #t = regression.predict(array([[cpu_percentage,cpu_time,m_available,m_swap,net_traffic,
                    #                       transmission_capture,transmission_observer]], dtype=float))
                    
                    #t = regression.predict(array([[cpu_percentage,cpu_time,m_available,m_swap,frame_rate]], dtype=float))
                    #print(t)
                    poolSplit = str(data.split(',')[-1]).split(']')[0]
                    pool = poolSplit.split()[0]
                    #print(pool)
                    features = array([[cpu_percentage, cpu_time, m_available, m_swap, frame_rate]], dtype=float)
                    t = model_ufmg.predict(features) if pool == "\'UFMG\'" else model_ufrgs.predict(features)
                    #print(t)
                    pools[pool] = t
                    #pools[poolSplit]
                    print(pools)

                    #migrate(pools, args.x/args.fps)
                    # Add output channel for response
                    #print(regression.predict([[1.7,2014202.7,3940237312,89915392,0.0001804828643798828,1547732123.2172844,1547732122.9963086
                  
                    if s not in outputs:
                        outputs.append(s)

                else:
                    # Interpret empty result as closed connection
                    #print >>sys.stderr, 'closing', client_address, 'after reading no data'
                    # Stop listening for input on the connection
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    # Remove message queue
                    #del message_queues[s]
