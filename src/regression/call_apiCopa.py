import requests
import json
import threading
import time 

class APICopa(object):
    """docstring for APICopa"""
    def __init__(self):


        #URL do Copa com a Porta para acesso RESTful
        self.copaUrl = 'http://copaserver:8000/'

        #Pool onde o server de video começa
        self.poolStart = 'Server2'

        #Pool para onde o server de video deve ser migrado
        self.poolDestiny = 'Server1'

        #Nome do container do server de video
        self.containerName = 'landoserver'
        
        

def migrateContainer():
    print("Starting Migration")
    self.data = {
    "container_name": self.containerName,
    "container_pool": self.poolStart,
    "destination_pool": self.poolDestiny,
    "operation": "migrate"
    }
    result = requests.post(self.copaUrl+'REST/container', self.data).json()
    print(result) 

