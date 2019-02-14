#!/usr/bin/env python
'''
########################################################
##         FEDERAL UNIVERSITY OF MINAS GERAIS         ##
##             COMPUTER SCIENCE DEPARTMENT            ##
##             WIRELESS NETWORKS LABORATORY           ##
##                                                    ##
##     Author: Fabio Alves Pereira                    ##
##     Obs.: Change the .environment file with the    ##
##         COPA SERVER ip address                     ##
########################################################
'''
class CopaApiController:

    def __init__(self, resource_url):
        self.base_url = open('config/.environment', 'r' 
                             ).readline().split('=')[1]
        self.resource_url = resource_url 