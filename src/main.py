#!/usr/bin/python3.6
from regression import Regression
from regression import REG_ALGORITHMS
import csv
import numpy as np
import argparse
import socket
import sys
import select
#import Queue
from multiprocessing import Queue

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
    regression = Regression(args.input, args.algorithm, args.features)
    regression.fit()
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
                data = s.recv(1024)
                if data:
                    
                    #print(data)
                    # A readable client socket has data
                    #print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
                    #message_queues[s].put(data)
                    #print(data)
                    cpu_percentage__ = data.split(',')[0]
                    cpu_percentage = str(cpu_percentage__).split('[')[1]
                    cpu_time = data.split(',')[1]
                    m_available = data.split(',')[2]
                    m_swap = data.split(',')[3]
                    net_traffic = data.split(',')[4]
                    transmission_capture = data.split(',')[5]
                    transmission_observer = data.split(',')[6]                        
                    
                    t = regression.predict([[cpu_percentage,cpu_time,m_available,m_swap,net_traffic,transmission_capture,transmission_observer]])
                    print(t)
                    poolSplit = str(data.split(',')[-1]).split(']')[0]
                    pool = poolSplit.split()[0]
                    print(pool)
                    pools[pool] = t
                    #pools[poolSplit]
                    print(pools)
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


