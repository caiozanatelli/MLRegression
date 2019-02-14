#!/usr/bin/env python
'''
########################################################
##         FEDERAL UNIVERSITY OF MINAS GERAIS         ##
##             COMPUTER SCIENCE DEPARTMENT            ##
##             WIRELESS NETWORKS LABORATORY           ##
##                                                    ##
##     Author: Fabio Alves Pereira                    ##
##                                                    ##
########################################################
'''

import requests
from api_controller import CopaApiController

class RestContainer(CopaApiController):

    def __init__(self):
        super(RestContainer, self).__init__('/container')

    def get_body(self, name, source, destination):
        return {
                'container_name': name,
                'container_pool': source,
                'destination_pool': destination,
                'operation': 'migrate',
            }

    def migrate(self, name, source, destination):
        return requests.post(self.base_url + self.resource_url, self.get_body(name, source, destination)).json()

#Example
print (RestContainer().migrate('container-name', 'origin', 'destination'))
