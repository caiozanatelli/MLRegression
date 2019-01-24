'''
########################################################
##         FEDERAL UNIVERSITY OF MINAS GERAIS         ##
##             COMPUTER SCIENCE DEPARTMENT            ##
##             WIRELESS NETWORKS LABORATORY           ##
##                                                    ##
##          Author: Marcos Magno de Carvalho          ##
##                                                    ##
########################################################
'''
from pylab import *
import numpy
import matplotlib.pyplot as plt

grupos = 7
Weka = [0.127028963683,0.191305849453,0.134736767148,0.330099710547,0.484438030701, 0.137449474517, 0.488797413613]

# nnet 0.127028963683
# svr 0.191305849453
# nusvr 0.134736767148
# dt 0.330099710547
# gbrt 0.484438030701
# knn 0.137449474517
# rfr 0.488797413613


fig, ax = plt.subplots()
indice = np.arange(grupos)
bar_larg = 0.4
transp = 0.7


plt.bar(indice + bar_larg, Weka, bar_larg, alpha=transp, color="#ffffff", hatch="/", edgecolor='black')

#plt.xlabel('Celulares', fontsize=16) 
plt.ylabel('(RMSE) % ', fontsize=16)
#plt.title('Notas por pessoa') 
plt.tick_params(axis='both', which='major')
plt.xticks(indice + bar_larg, ('NNet', 'SVR', 'NuSVR', 'DT', 'GBRT', 'KNN', 'RFR'))
 
plt.tight_layout() 
plt.show()