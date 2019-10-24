#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import tensorflow as tf
import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
import numba as nb
import sys
import openseespy.opensees as ospy


# In[2]:


ospy.version()


# In[3]:


#targNumpy = 'cuda'
targNumpy = 'parallel'


# In[4]:


@nb.vectorize(["float64(int64,int64,int64,float64)"], target= targNumpy)
def coordX(M, vx, vy, dx):
    if M <  ( (vx+1) * (vy+1) ):
        return  (M % (vx+1) ) * (dx)
    else:
        return  ( ( M - (vx+1) * (vy+1) ) % (vx*2 +1) ) * (dx/2) 


# In[5]:


@nb.vectorize(["float64(int64,int64,int64,float64)"], target= targNumpy)
def coordY(M, vx, vy, dy):
    if M <  ( (vx+1)* (vy+1) ):
        return  ((M % ( (vx+1) * (vy+1) )// (vx+1) ) ) * (dy)
    else:
        return  ( ((M - (vx+1) * (vy+1) ) % ( (vx*2 +1) * (vy*2 +1) ))// (vx*2 +1) ) * (dy/2)


# In[6]:


@nb.vectorize(["float64(int64,int64,int64,float64)"], target= targNumpy)
def coordZ(M, vx, vy, dz):
    if M < ( (vx+1)* (vy+1) ):
        return  0.0
    else:
        return  (((M - ( (vx+1)* (vy+1) ) ) // ( (vx*2 +1)*(vy*2 +1))) + 1) * (dz)


# In[7]:


@nb.jit(["void(int32,float64,float64,float64)"], parallel = True)
def ospyNode(M, cx, cy, cz):
    for i in nb.prange(M.size):
        ospy.node(int(M[i]),cx[i],cy[i],cz[i])
        if cz[i] == 0.0:
            ospy.fix(int(M[i]), 1, 1, 1, 1, 1, 1)


# In[8]:


@nb.jit(["void()"])
def resetModel():
    # - Modelo Openseespy
    ospy.wipe()
    # init model
    # degrees of freedom by node
    ndf=6
    ospy.model('basic', '-ndm', 3, '-ndf', ndf)
    # transformações geometricas
    ospy.geomTransf('Linear', 1, 0.0, 0.0, 1.0, '-jntOffset', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    ospy.geomTransf('Linear', 2, 1.0, 0.0, 0.0, '-jntOffset', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0) 
    


# In[9]:


@nb.jit(["void(int64,float64,int64,float64,int64,float64)"])
def estruct(vx, dx, vy, dy, vz, dz):
    # numero total de pontos
    Npts = (vx*2 +1) * (vy*2 +1) * (vz) + ( (vx+1) * (vy+1) )
    # Matriz dos indices
    mat = np.arange(0,Npts, 1, dtype= np.int64 )
    # corrdenadas dos pontos
    cX = coordX(mat, vx, vy, dx)
    cY = coordY(mat, vx, vy, dy)
    cZ = coordZ(mat, vx, vy, dz)
    # matriz dos andares superiores
    matA = mat[(vX+1)*(vY+1)::].reshape(vZ, vY*2 +1, vX*2 +1)
    # matriz dos indices iniciais das vigas em x
    matXI = matA[::,::2,:-1:]
    # matriz dos indides finais das vigas em x
    matXF = matA[::,::2,1::]
    # matriz dos indices inicias das vigas em Y
    matYI = matA[::,:-1:,::2]
    # matriz dos indices finais das vigas em Y
    matYF = matA[::,1::,::2]
    # matriz pontos da fundação
    matB = mat[: (vx+1) * (vy+1)]
    # matriz final dos pilares
    matPF = matA[::,::2,::2]
    # matriz inicial dos pilares
    matPI = np.append(matB,matPF[:-1:,::,::]).reshape(vZ,(vY+1),(vX+1))
    # Matrizes de superficie 
    matBL = matA[::, :-1:, :-1:]
    #print("Inferior esquerdo\n",matBL)
    matBR = matA[::, :-1:, 1::]
    #print("Inferior direito\n",matBR)
    matTL= matA[::, 1::, :-1:]
    #print("Superior esquerdo\n",matTL)
    matTR = matA[::, 1::, 1::]
    #print("Superior direito\n",matTR)
    
    # reset model
    resetModel()
    # nodes
    ospyNode(mat, cX, cY, cZ)
    
    return  matPI, matPF , matXI,  matXF,  matYI,  matYF, matBL, matBR, matTL, matTR


# In[10]:


# entradas
# numero de vaos em x
vX = 2
# distancia dos vaos em x
dX = 5.25
# número de vãos em y
vY = 3
# distancia dos vaos em y
dY = 7.25
# numero pavimentos
vZ = 2
 # distancia piso a piso
dZ = 3.25


# In[11]:



matPI, matPF , matXI,  matXF,  matYI,  matYF, matBL, matBR, matTL, matTR = estruct(vX, dX, vY, dY, vZ, dZ)


# In[12]:


teste = ospy.nodeCoord(40)
print(teste)


# In[13]:


b = .15 # base do elemento estrutural
h = .4 # altura do elemento estrutural
fck = 30 #FCK
ni = 0.2 # coeficiente de Poisson


# In[14]:



A = b*h # area do elemento
E = .85*5600*fck**.5 # modulo de elasticidade - Young modulos
G = E/(2*(1+ni)) # modulo de cisalhamento - shear modulus
J = ((b*h)/12) * (b**2 + h**2) # torsional moment of inertia of cross section
Iy = (b*h**3)/12 # second moment of area about the local z-axis
Iz = (h*b**3)/12 # second moment of area about the local y-axis


# In[15]:


ospy.element('elasticBeamColumn', 1 , int(matXI[0][0][0]), int(matXF[0][0][0]), A, E, G, J, Iy, Iz, 1,  '-mass', 0.0,  '-cMass')


# In[16]:


type(matXI[0][0][0])


# In[17]:


matXF.size


# In[18]:


[matXI[0][0][0],matXF[0][0][0]]

