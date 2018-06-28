# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 19:51:00 2018

@author: ffrib
"""

from timeit import default_timer as timer




import sys
sys.path.append('C:/Tcl/')

from opensees import *

import numpy as np



start = timer()



# Destroy all constructed objects (clear all)
wipe()

# Model dimensions and Number of DOF's
ndf=6
model('basic', '-ndm', 3, '-ndf', ndf)


# Número de vãos Nx e Ny e Número de lajes Nz
Nx = 5
Ny = 2
Nz = 2


# Valor dos vãos de viga e distância entre pavimentos
Dx = 5.
Dy = 7.
Dz = 3.

# Definição da função com o Número de nós Npts e índice dos nós (tags) I
Npts = (Nx)*(Ny)*(Nz)
for I in range(0, Npts, 1):
    node(I, (I % Nx)*(Dx), ((I % (Nx*Ny))//Nx)*(Dy), ((I // (Nx*Ny)) + 1)*Dz)
   


#testando se os nós foram criados
a = nodeCoord(2)
print(a)

#Contador de tempo
dt = timer() - start
print ("O tempo de execucao foi de %f s" % dt)