#! python3
# -*- coding: utf-8 -*-

"""
Created on Fri Apr 20 11:57:56 2018

@author: ffrib
"""

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
avX = np.arange(po, 1 + po + (nX * stpX) , stpX , dtype= float)
print(avX)
# aux vec Y
avY = np.arange(po, 1 + po + (nY * stpY) , stpY , dtype= float)
print(avY)
# aux vec Z
avZ = np.arange(po, 1 + po + (nZ * ffd) , ffd , dtype= float)
print(avZ)

# %%
