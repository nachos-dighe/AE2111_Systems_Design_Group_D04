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

# Counters
i = 0 
j = 0 
k = 0

t = 1 # Needs to be defined somewhere!! (not here)

G = 26*(10**9)     # http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma6061t6
E = 207*(10**9)    # http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma6061t6


CG_XList = []
CG_ZList = []
Ix_totalList = []
Iz_totalList = []
ylst = []

SpanTab = []
Ixtab = [] 
Iytab = []
Jlist = []


import Deflection as Deflection
import Rotationangle as RotAngle
import Chord_Length as Lengths
import CG_wingboxFRANK as CG
import Moment_of_Inertia as MOI
import Stringers_MOI as Stringer_MOI
import Torsional_stiffness as PMOI


##nr_top = int(input("How many stringers are we using at the top? "))
##nr_bot = int(input("How many stringers are we using at the bottem? "))
##
##if nr_top and nr_bot !=0 :
##    L_s = int(input("What is the length of the symetric stringers? "))
##    t_s = int(input("What is the thickness of the stringers? "))
    

with open("ylstFRANK.dat", "r") as file : # Reads the y position file 
    ylstRAW = file.readlines()
    
for line in ylstRAW :
    y = line.replace("\n", "")
    ylst.append(y)

alpha, beta, b, DeltaX, Cr = Lengths.WingboxDimensions(RCr, TCr, Span, ylst) # All geometry is now defined togheter with ylst

while (dT * i)<= Span/2 :  # Calculates the CG position in CG_XList 
    CG_x, CG_z = CG.cg_calculation(alpha, beta, b[i], DeltaX[i])
    CG_XList.append(CG_x)
    CG_ZList.append(CG_z)
    i = i + 1

tRot= 0.01
# tRot, is the minimum thichness requierd to achieve the rotational requierment
while True :
    tRot = tRot + 0.001 
    i = 0
    while i <= 999 :
        J = PMOI.J_calculation(alpha, beta, b[i], DeltaX[i], t)
        Jlist.append(J)
        i = i + 1
        
    rot_lst = RotAngle.rotation(T_lst, Jlst, G, ylst)
    MaxRot = max(rot_lst)
    if MaxRot >= 0.05:
        break 
    j = j + 1



while (dT * k)<= Span/2 :
    tMin, IXX = MOI.thickness_calculator(DeltaX[k],beta, alpha, CG_ZList[k], b[k], Ixx_required)
    
    k = k + 1





##plt.subplot(111)
##plt.plot(SpanTab, Ix_totalList)
##plt.title("The moment of inertia of the X against the span")
##plt.xlabel("The y coordinate of half a wing [m]")
##plt.ylabel("The second moment of area for in the x direction [m^4] ")




##plt.show()


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











