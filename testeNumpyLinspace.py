#! python3
# -*- coding: utf-8 -*-

"""
Created on Fri Apr 20 11:57:56 2018

@author: ffrib
"""
#%% imports
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# %% start point
po = 0.0

# %% Parameters
# spans size

stpX = 2.5
stpY = stpX

# number of spans
nX = 10
nY = 12

# floor to floor distance
ffd = 3.2

# number of floors
nZ = 5

# %% Creating auxiliary vectors
# aux vec X
avX = np.linspace(po, po + (nX * stpX) , num = nX + 1 , dtype= float)
print(avX)
# aux vec Y
avY = np.linspace(po, po + (nY * stpY) , num = nY + 1, dtype= float )
print(avY)
# aux vec Z
avZ = np.linspace(po, po + (nZ * ffd) , num = nZ + 1 , dtype= float)
print(avZ)

# %%
