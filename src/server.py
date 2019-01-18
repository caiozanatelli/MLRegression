import select
import socket
import sys
import Queue
import logging
import time

class Server(object):
    """docstring for Connection"""
    def __init__(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.setblocking(0)
        self.__server_address = ('150.164.10.58', 10001)
        self.__server.bind(self.__server_address)
        self.__server.listen(5)
        self.__inputs = [self.__server]
        self.__outputs = [ ]        
        self.__message_queues = {}
        

    def handleConnection(self):
        while self.__inputs:            
            # Wait for at least one of the sockets to be ready for processing
            print >>sys.stderr, '\nwaiting for the next event'
            readable, writable, exceptional = select.select(self.__inputs, self.__outputs, self.__inputs)
            # Handle inputs
            for s in readable:
                if s is self.__server:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = s.accept()
                    print >>sys.stderr, 'new connection from', client_address
                    connection.setblocking(0)
                    self.__inputs.append(connection)

                    # Give the connection a queue for data we want to send
                    self.__message_queues[connection] = Queue.Queue()
                else:
                    data = s.recv(1024)
                    if data:
                        # A readable client socket has data
                        #print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
                        self.__message_queues[s].put(data)
                        #print(data)
                        cpu_percentage__ = data.split(',')[0]
                        cpu_percentage = str(cpu_percentage__).split('[')[1]
                        cpu_time = data.split(',')[1]
                        m_available = data.split(',')[2]
                        m_swap = data.split(',')[3]
                        net_traffic = data.split(',')[4]
                        transmission_capture = data.split(',')[5]
                        transmission_observer = data.split(',')[6]                        

                        # Add output channel for response
                        if s not in self.__outputs:
                            self.__outputs.append(s)             
                    else:
                        # Interpret empty result as closed connection
                        print >>sys.stderr, 'closing', client_address, 'after reading no data'
                        # Stop listening for input on the connection
                        if s in self.__outputs:
                            self.__outputs.remove(s)
                        self.__inputs.remove(s)
                        s.close()
                        # Remove message queue
                        del self.__message_queues[s]


            
    def splitMsg(self,data):
        cpu_percentage__ = data.split(',')[0]
        cpu_percentage = str(cpu_percentage__).split('[')[1]
        cpu_time = data.split(',')[1]
        m_available = data.split(',')[2]
        m_swap = data.split(',')[3]
        net_traffic = data.split(',')[4]
        transmission_capture = data.split(',')[5]
        transmission_observer = data.split(',')[6]
        """
        print('cpu_percentage', cpu_percentage)
        print('cpu_time', cpu_time)
        print('m_available', m_available)
        print('m_swap', m_swap)
        print('net_traffic', net_traffic)
        print('transmission_capture', transmission_capture)
        print('transmission_observer', transmission_observer)
        """
        
        
       
        
    
    def getData(self):
        return cpu_percentage,cpu_time,m_available,m_swap,net_traffic,transmission_capture,transmission_observer

        




        