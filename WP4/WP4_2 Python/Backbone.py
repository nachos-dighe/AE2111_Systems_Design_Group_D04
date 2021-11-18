import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

from math import tan
import math

# Geometric
RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 0.1
i = 0 
j = 0 

CG_XList = []
CG_ZList = []
Ix_totalList = []
Iy_totalList = []

SpanTab = []
Ixtab = [] 
Iytab = []

import Chord_Length as Lengths
import CG_wingbox as CG
import Moment_of_Inertia as MoI


Theta2, Theta3, b2, DeltaX, Cr, y = Lengths.WingboxDimensions(RCr, TCr, Span, dT)

while (dT * i)<= Span/2 :
    CG_x, CG_z = CG.cg_calculation(Theta2, Theta3, b2[i], DeltaX[i])
    CG_XList.append(CG_x)
    CG_ZList.append(CG_z)
    i = i +1

t = 1 # Needs to be defined somewhere!! (not here)


while (dT * j)<= Span/2 :
    Ix_total = MoI.Ixcalculator(DeltaX[j],b2[j],Theta2,Theta3,t,CG_XList[j],CG_ZList[j])
#    Iz_total = MoI.Izcalculator(DeltaX[j],b2[j],Theta2,Theta3,t,CG_XList[j],CG_ZList[j])
    Ix_totalList.append(Ix_total)
#    Iz_totalList.append(Iz_total)
    SpanTab.append(dT * j)
    j = j + 1


plt.subplot(211)
plt.plot(SpanTab, Ix_totalList)
plt.title("The moment of inertia of the X against the span")

#plt.subplot(212)
#plt.plot(SpanTab, Iz_totalList)
#plt.title("The moment of inertia of the Z against the span")

plt.show()


# Note to myself (Frank)
# [V] Fix the bug that casues Berkes code (MoI calc) to not work with this backbone
# [V] I changed the degrees from my code to radians, check it!
# [ ] Think how you want your resutls to end up, do you want a list and if so, which values do you want to know
# [ ] Think how to inplement the data from WP4.1 load diagrams
# [ ] Putting the stringer MoI in backbone
# [ ] Making all the values in the other code use the same name
# [ ] Making the graphs more nice
# [ ] Putting formulas in the code (Lynn)
#  
#










