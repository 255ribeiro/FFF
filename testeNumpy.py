# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:57:56 2018

@author: ffrib
"""

import numpy as np
import matplotlib.pyplot as plt


#%%

# ponto inicial
po = 0
#tamanho do passo
stp = 2.5
#número de intervalos
nX = 10
nY = 20
# criando vetor de medidas equidistantes
mvX = np.linspace(po, po+ (nX * stp) , num = nX +stp )

mvY = np.linspace(po, po+ (nY * stp) , num = nY +stp )
#%%


xx = np.meshgrid(mvX,mvX).reshape(2,-1).T
print(xx)

