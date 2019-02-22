import requests
import json
import threading
import time 

class APICopa(object):
    """docstring for APICopa"""
    def __init__(self):

        #URL do Copa com a Porta para acesso RESTful
        self.copaUrl = 'http://copaserver:8000/'
        #Nome do container do server de video
        self.containerName = 'landoserver'
        
def migrateContainer(poolStart, poolDestiny):
    print("Starting Migration")
    self.data = {
        "container_name": self.containerName,
        "container_pool": poolStart,
        "destination_pool": poolDestiny,
        "operation": "migrate"
    }
    result = requests.post(self.copaUrl+'REST/container', self.data).json()
    print(result) 
