# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 17:11:01 2018

@author: Felipe
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
Nx=Nx+1
Ny=Ny+1

# Valor dos vãos de viga e distância entre pavimentos
Dx = 5.
Dy = 7.
Dz = 3.

# Definição da função com o Número de nós Npts e índice dos nós (tags) I
Npts = Nx*Ny*Nz
I = np.arange(0, Npts, 1)
X = (I % Nx)*Dx
Y = ((I % (Nx*Ny))//Nx)*Dy
Z = ((I // (Nx*Ny)) + 1)*Dz

# Loop para criação dos nós do modelo em EF
for i in range(Npts):
#    node(int(I[i]), float((I[i] % Nx)*Dx), float(((I[i] % (Nx*Ny))//Nx)*Dy), float(((I[i] // (Nx*Ny)) + 1)*Dz))
    node(int(I[i]), float(X[i]), float(Y[i]), float(Z[i]))

# testando se os nós foram criados
a = nodeCoord(2)
print(a)




#Contador de tempo
dt = timer() - start
print ("O tempo de execucao foi de %f s" % dt)