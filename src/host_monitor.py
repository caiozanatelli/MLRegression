#!/usr/bin/env python
'''
    Autora: Fernanda Aparecida Rodrigues Silva
    -------------------------------------
    WINET - Wireless Networks Laboratory
    Departamento de Ciencia da Computacao
    Universidade Federal de Minas Gerais

'''
# IMPORTS
import os
import time
import psutil
import subprocess
import socket
import sys
import argparse

class HostMonitor():
    labels = ["cpu_percentage",
              "cpu_time",
              #"cpu_count",
              #"m_percentage",
              "m_available",
              #"m_size",
              "m_swap",
              "net_traffic",
              "time_between_frames_in",
              "time_between_frames_out"]

    num_vars = len(labels)
    results = {}
    CAPTURE = "cbtm@192.168.0.52"
    OBSERVER = "winet@192.168.0.13"
    frame_file = "~/frame.png"

    def __init__(self):
        for label in self.labels:
            self.results[label] = 0

    def convert_dict_to_list(self, results):
        results_list = []
        for label in self.labels:
            results_list.append(self.results[label])
        return results_list

    def get_time_between_frames(self):
        devnull = open(os.devnull, 'w')
        init_time = time.time()
        #res = subprocess.run(['scp', self.CAPTURE + ":" + self.frame_file, '.'], stdout=devnull)
        last_time = time.time() - init_time
        self.results["time_between_frames_in"] = last_time
        init_time = time.time()
        #res = subprocess.run(['scp', "frame.png", self.OBSERVER + ":~/"], stdout=devnull)
        last_time = time.time() - init_time
        self.results["time_between_frames_out"] = last_time
        devnull.close()
        print(self.results)

    def read_data(self):
        # isNewFile = False
        # try:
        #     file_pointer = open("database.csv", 'r')
        # except IOError:
        #     isNewFile = True
        # if(isNewFile is False):
        #     file_pointer.close()

        # file_pointer = open("database.csv", 'a')
        # writer = csv.writer(file_pointer, delimiter=',')
        # if(isNewFile is True):
        #     writer.writerow(self.labels)

        network_reference = psutil.net_io_counters().bytes_sent
        network_reference += psutil.net_io_counters().bytes_recv

        # CPU Usage
        self.results["cpu_percentage"] = psutil.cpu_percent(interval=None)
        self.results["cpu_time"] = psutil.cpu_times(percpu=None).idle
        #self.results["cpu_count"] = psutil.cpu_count()

        # Memory Usage
        #self.results["m_percentage"] = psutil.virtual_memory().percent
        self.results["m_available"] = psutil.virtual_memory().available
        #self.results["m_size"] = psutil.virtual_memory().total
        self.results["m_swap"] = psutil.swap_memory().used

        # Network
        network_traffic = psutil.net_io_counters().bytes_sent
        network_traffic += psutil.net_io_counters().bytes_recv
        self.results["net_traffic"] = (network_traffic - network_reference)
        self.results["net_traffic"] /= 1048576. * 8

        # Processing
        self.get_time_between_frames()
        return self.convert_dict_to_list(self.results)


class ClientSocket(object):
    """docstring for ClientSocket"""
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_address = ('150.164.10.58', 10001)    
        self.__socket.connect(self.__server_address)

    def sendData(self,data, pool):        
        try:
            # Send data
            message = data
            message.append(pool)
            
            self.__socket.sendto(bytes(str(message), "utf-8"), self.__server_address)
        finally:
            #print >>sys.stderr, 'closing socket'
            self.__socket.close()        


    

if __name__ == '__main__':


    def parse_args():
        parser = argparse.ArgumentParser(description='Host Monitor')

        parser.add_argument('-l', '--host', action='store', type=str, required=True,
                            help='Host name')
        return parser.parse_args()

    args = parse_args()    
    m = HostMonitor()
    


    while True:
        clientSocket = ClientSocket()
        datatoSend = m.read_data()
        clientSocket.sendData(datatoSend, args.host)
        print(datatoSend)
        time.sleep(2)

