import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


from math import *


# Geometric
RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 0.1
i = 0 
j = 0 

t = 1 # Needs to be defined somewhere!! (not here)

CG_XList = []
CG_ZList = []
Ix_totalList = []
Iz_totalList = []
ylst = []

SpanTab = []
Ixtab = [] 
Iytab = []

import Deflection as Deflection
import Rotationangle as RotAngle
import Chord_Length as Lengths
import CG_wingboxFRANK as CG
import Moment_of_Inertia as MOI
import Stringers_MOI as Stringer_MOI

nr_top = int(input("How many stringers are we using at the top? "))
nr_bot = int(input("How many stringers are we using at the bottem? "))

if nr_top and nr_bot !=0 :
    L_s = int(input("What is the tichness ofthe stringers? "))

with open("ylstFRANK.dat", "r") as file :
    ylstRAW = file.readlines()
    
for line in ylstRAW :
    y = line.replace("\n", "")
    ylst.append(y)

alpha, beta, b, DeltaX, Cr = Lengths.WingboxDimensions(RCr, TCr, Span, ylst) # All geometry is now defined togheter with ylst

while (dT * i)<= Span/2 :  # Calculates the CG position in CG_XList and CG_XList
    CG_x, CG_z = CG.cg_calculation(alpha, beta, b[i], DeltaX[i])
    CG_XList.append(CG_x)
    CG_ZList.append(CG_z)
    i = i + 1

while (dT * j)<= Span/2 :
    tMin, IXX = MOI.thickness_calculator(DeltaX[j],beta, alpha,CG_XList[j], CG_ZList[j], b[j])
    
##    Ix_totalList.append(Ix_total)
##    SpanTab.append(dT * j)
    j = j + 1





##plt.subplot(111)
##plt.plot(SpanTab, Ix_totalList)
##plt.title("The moment of inertia of the X against the span")
##plt.xlabel("The y coordinate of half a wing [m]")
##plt.ylabel("The second moment of area for in the x direction [m^4] ")




plt.show()


# Note to myself (Frank)
# [V] Fix the bug that casues Berkes code (MoI calc) to not work with this backbone
# [V] I changed the degrees from my code to radians, check it!
# [ ] Think how you want your resutls to end up, do you want a list and if so, which values do you want to know
# [ ] Think how to inplement the data from WP4.1 load diagrams
# [ ] Putting the stringer MoI in backbone
# [V] Making all the values in the other code use the same name
# [ ] Making the graphs more nice
# [ ] Putting formulas in the code (Lynn)
# [ ] Making a way to put the input for the strinegrs nicely











