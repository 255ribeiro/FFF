import sys
sys.path.append('C:/Tcl/')

from opensees import *
from math import asin, sqrt

import numpy as np
import matplotlib.pyplot as plt

import time
start = time.time()


# set some properties
wipe()

#model dimensions and Ndof's
ndf=6
model('basic', '-ndm', 3, '-ndf', ndf)

# Reinforced concrete constants
fck=30.0
E = 0.85*5600*((fck)**(1/2))*1.0E+06
G=E/2.4

# Cross-section constants
# For beams
A_b=1000.0E-04
Iz_b=208333.33E-08
Iy_b=33333.33E-08
J_b= 99747.0E-08 #VERIFICAR EXPRESSÃO PARA CALCULAR O J

# For columns
A_c=400.0E-04
Iz_c=13333.33E-08
Iy_c=13333.33E-08
J_c= 22493.29E-08 #VERIFICAR EXPRESSÃO PARA CALCULAR O J

MemberType = {
    'Beam': [A_b, Iy_b, Iz_b, J_b],
    'Column': [A_c, Iy_c, Iz_c, J_c]
}


# procedure to read - DEFINITION OF ELEMENT
def ElasticBeamColumn(eleTag, iNode, jNode, sectType, E, G, transfTag, M, massType):

    found = 0

    prop = MemberType[sectType]

    A = prop[0]
    Iy = prop[1]
    Iz = prop[2]
    J = prop[3]
    element('elasticBeamColumn', eleTag, iNode, jNode, A, E, G, J, Iy, Iz, transfTag, '-mass', M, massType)

# Frame dimensions
L=5.0
H=3.0

# Model nodes
node(1, 0.0, 0.0, 0.0)
node(2, 0.0, 0.0, H/2)
node(3, 0.0, 0.0, H)
node(4, L,   0.0, 0.0)
node(5, L,   0.0, H/2)
node(6, L,   0.0, H)
node(7, L,   L,   0.0)
node(8, L,   L,   H)
node(9, L,   L,   H/2)
node(10, 0.0, L,   0.0)
node(11, 0.0, L,   H/2)
node(12, 0.0, L,   H)

node(13, 0.5*L, 0.0, H)
node(14, L, 0.5*L, H)
node(15, 0.5*L, L, H)
node(16, 0.0, 0.5*L, H)

node(17, 0.5*L, 0.5*L, H)

# Supports
fix(1, 1, 1, 1, 0, 0, 0)
fix(4, 1, 1, 1, 0, 0, 0)
fix(7, 1, 1, 1, 0, 0, 0)
fix(10, 1, 1, 1, 0, 0, 0)

# Rigid Diaphragm
cNodeTags = [3, 6, 9, 12, 13, 14, 15, 16]
rigidDiaphragm(3, 17, *cNodeTags)

# VERIFICAR QUAL O COMPORTAMENTO DO DIAFRAGMA E DO PÓRTICO SE ROTULAR A AS BARRAS FICTÍCIAS 
# QUE GERAM O DIAFRAGMA NO CONTATO COM O PÓRTICO. VER SE APOS ISTO AUMENTAR A RIGIDEZ DESTAS
# BARRAS MELHORA O COMPORTAMENTO.


# Creating the local coord. system 
# for columns
vecXZ = [0., 1., 0.]
offset = [0., 0., 0., 0., 0., 0.]
geomTransf('Linear', 1, *vecXZ, *offset)

# for beams X
vecXZ = [0., 1., 0.]
offset = [0., 0., 0., 0., 0., 0.]
geomTransf('Linear', 2, *vecXZ, *offset)

## for beams Y
vecXZ = [-1., 0., 0.]
offset = [0., 0., 0., 0., 0., 0.]
geomTransf('Linear', 3, *vecXZ, *offset)

# geomTransf Linear $transfTag $vecxzX $vecxzY $vecxzZ <-jntOffset $dXi $dYi $dZi $dXj $dYj $dZj>


# Element connectivity
# Columns
ElasticBeamColumn(1, 1, 2, 'Column', E, G, 1, 0., '-cMass')
ElasticBeamColumn(2, 2, 3, 'Column', E, G, 1, 0., '-cMass')
ElasticBeamColumn(3, 4, 5, 'Column', E, G, 1, 0., '-cMass')
ElasticBeamColumn(4, 5, 6, 'Column', E, G, 1, 0., '-cMass')
ElasticBeamColumn(5, 7, 8, 'Column', E, G, 1, 0., '-cMass')
ElasticBeamColumn(6, 8, 9, 'Column', E, G, 1, 0., '-cMass')
ElasticBeamColumn(7, 10, 11, 'Column', E, G, 1, 0., '-cMass')
ElasticBeamColumn(8, 11, 12, 'Column', E, G, 1, 0., '-cMass')

# Beams X
ElasticBeamColumn(9, 3, 13, 'Beam', E, G, 2, 0., '-cMass')
ElasticBeamColumn(10, 13, 6, 'Beam', E, G, 2, 0., '-cMass')
ElasticBeamColumn(11, 12, 15, 'Beam', E, G, 2, 0., '-cMass')
ElasticBeamColumn(12, 15, 9, 'Beam', E, G, 2, 0., '-cMass')

# Beams Y
ElasticBeamColumn(13, 3, 16, 'Beam', E, G, 3, 0., '-cMass')
ElasticBeamColumn(14, 16, 12, 'Beam', E, G, 3, 0., '-cMass')
ElasticBeamColumn(15, 6, 14, 'Beam', E, G, 3, 0., '-cMass')
ElasticBeamColumn(16, 14, 9, 'Beam', E, G, 3, 0., '-cMass')


# Diaphragm
ElasticBeamColumn(17, 3, 17, 'Beam', E, G, 2, 0., '-cMass')
ElasticBeamColumn(18, 17, 9, 'Beam', E, G, 2, 0., '-cMass')
ElasticBeamColumn(19, 6, 17, 'Beam', E, G, 2, 0., '-cMass')
ElasticBeamColumn(20, 17, 12, 'Beam', E, G, 2, 0., '-cMass')

#
# apply loads for static analysis & perform analysis
#

timeSeries('Linear', 1)
pattern('Plain', 1, 1) 
load(3, 0., 0., -10000.0E+03, 0., 0., 0.)
#load(3, 10.0E+03, 0., 0., 0., 0., 0.)

integrator('LoadControl', 1.0)
algorithm('Linear')
analysis('Static')
analyze(1)

# Output
ux3 = nodeDisp(3,1)*100
uy3 = nodeDisp(3,2)*100
uz3 = nodeDisp(3,3)*100

rx3 = nodeDisp(3,4)
ry3 = nodeDisp(3,5)
rz3 = nodeDisp(3,6)

esforcos=eleResponse(2,'forces')
esforcos2=eleForce(2, 9)*1.0E-03


end = time.time()
print('Tempo de Execucao =',end - start, 'segundos')