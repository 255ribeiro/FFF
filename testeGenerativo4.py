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
Nx0=Nx+1
Ny0=Ny+1
Nx=Nx*2 +1
Ny=Ny*2 +1

# Valor dos vãos de viga e distância entre pavimentos
Dx0 = 5.
Dy0 = 7.
Dz  = 3.
Dx  = Dx0*0.5
Dy  = Dy0*0.5

# Número de nós Npts e índice dos nós (tags) I
Npts = Nx*Ny*Nz
I = np.arange(0, Npts, 1)
I2= np.arange(0, Nx0*Ny0,1)
X = (I % Nx)*Dx
Y = ((I % (Nx*Ny))//Nx)*Dy
Z = ((I // (Nx*Ny)) + 1)*Dz
X0 = (I2 % Nx0)*Dx0
Y0 = ((I2 % (Nx0*Ny0))//Nx0)*Dy0

# Loop para criação dos nós do modelo em EF
for i in range(Npts):
#    node(int(I[i]), float((I[i] % Nx)*Dx), float(((I[i] % (Nx*Ny))//Nx)*Dy), float(((I[i] // (Nx*Ny)) + 1)*Dz))
    node(int(I[i]), float(X[i]), float(Y[i]), float(Z[i]))
    if i<Nx0*Ny0:
        node(int(I[len(I)-1]+1+I2[i]), float(X0[i]), float(Y0[i]), 0.0)
    

teste = nodeCoord(127)

#Contador de tempo
dt = timer() - start
print ("O tempo de execucao foi de %f s" % dt)