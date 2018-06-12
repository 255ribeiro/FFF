import numpy as np

from timeit import default_timer as timer

from numba import cuda

from numba import vectorize

from numba import njit

from numba import jit

from numba import autojit

start = timer()


# VERIFICAR A HIPÓTESE DE SEPARADAMENTE GERAR ESSES GRIDS DE COORDENADAS DE PONTOS
# GRAVÁ-LOS EM ARQUIVO NO DISCO E LÊ-LOS SEPARADAMENTE. SERIA MAIS RÁPIDO DO QUE
# ENCHER ESSES VETORES EM CADA INSTANCIAÇÃO DO MODELO PARAMÉTRICO?

#@njit
#@njit kwargs
@jit
#@autojit
#@vectorize(['float32(float32, float32, float32)'], target='cuda')
#@cuda.jit(device=True)
def pontos(x_p, y_p, z_p):
    npoints = len(x_p) * len(y_p) * len(z_p)
    points = np.zeros((npoints, 3))
    i = 0
    nx = len(x_p)
    for z in z_p:
        for y in y_p:
            points[i:i+nx, 0] = x_p
            points[i:i+nx, 1] = y
            points[i:i+nx, 2] = z
            i += nx

    return points


Lx=5.
Ly=6.
Hpav=3.

Nrep=100

nx = range(1,Nrep)
ny = range(1,Nrep)
nz = range(1,Nrep)

cont=0
for k in range(1,Nrep,1):

    Nx = nx[k-1]
    Ny = ny[k-1]
    Nz = nz[k-1]
    ex=0.5*Lx
    ey=0.5*Ly

    Vx = np.r_[0:Nx+1] * ex
    Vy = np.r_[0:Ny+1] * ey
    Vz = np.r_[1:Nz+1] * Hpav

    Pxyz = pontos(Vx, Vy, Vz)
    cont=cont+1

#Contador 2
dt = timer() - start
print ("O tempo de execucao foi de %f s" % dt)
