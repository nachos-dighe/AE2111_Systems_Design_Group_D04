import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


from math import *


#---------------------------------------------------------------------------------------------


# Geometric
RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 0.1

# Counters
i = 0 
j = 0 
k = 0

# The begin tichness which we than slowly increase until it matches requirement
tRot= 0.0001
tDef = 0.00001

MaxRotReq = (10*0.0174532952) / 1.5 # This is the max required rotation angle times the safety factor
MaxDefReq = (Span *0.15) / 1.5 # This is the max required deflection times the safety factor

G = 26*(10**9)     # http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma6061t6
E = 207*(10**9)    # http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma6061t6

# Defining lists
CG_XList = []
CG_ZList = []
Ix_totalList = []
Iz_totalList = []
ylst = []
T_lst = []
M_lst = []

# Defining lists for graphs
SpanTab = []
Ixtab = [] 
Iytab = []
Jlist = []

#---------------------------------------------------------------------------------------------


import Deflection as Deflection
import Rotationangle as RotAngle
import Chord_Length as Lengths
import CG_wingboxFRANK as CG
import Moment_of_Inertia_FRANK as MOI
import Stringers_MOI as Stringer_MOI
import Torsional_stiffness as PMOI


#---------------------------------------------------------------------------------------------
# Input for which laod case and for stringers


LoadChoice = input(" Which load case do you want to evaluate?\nPos_Crit?(1)\nNeg_crit?(2)")
StringersBoolean = True 

if StringersBoolean == True:
    nr_top = int(input("How many stringers are we using at the top? "))
    nr_bot = int(input("How many stringers are we using at the bottem? "))

    if nr_top and nr_bot !=0 :
        L_s = float(input("What is the length of the symetric stringers? "))
        t_s = float(input("What is the thickness of the stringers? "))
        


#---------------------------------------------------------------------------------------------
# Reading files to get the spanwise coordniates, bending loads and torisonal loads and determinign the geometry of the wingbox


with open("ylstFRANK.dat", "r") as file : # Reads the y position file 
    ylstRAW = file.readlines()

for line in ylstRAW :
    y = line.replace("\n", "")
    y = float(y)
    ylst.append(y)


if "1" in LoadChoice:
    with open("Critical_Load_Torsion_Pos_Crit.dat", "r") as file : 
        T_lstRAW = file.readlines()
    with open("Critical_Load_Bending_Pos_Crit.dat", "r") as file : 
        M_lstRAW = file.readlines()

if "2" in LoadChoice:
    with open("Critical_Load_Torsion_Neg_Crit.dat", "r") as file : 
        T_lstRAW = file.readlines()
    with open("Critical_Load_Bending_Neg_Crit.dat", "r") as file : 
        M_lstRAW = file.readlines()    

for line in T_lstRAW :
    T = line.replace("\n", "")
    T = float(T)
    T_lst.append(T)
    
for line in M_lstRAW :
    M = line.replace("\n", "")
    M = float(M)
    M_lst.append(M)  

alpha, beta, b, DeltaX, Cr = Lengths.WingboxDimensions(RCr, TCr, Span, ylst) # All geometry is now defined togheter with ylst

#---------------------------------------------------------------------------------------------


while i<= 999 :  # Calculates the CG position in CG_XList 
    CG_x, CG_z = CG.cg_calculation(alpha, beta, b[i], DeltaX[i])
    CG_XList.append(CG_x)
    CG_ZList.append(CG_z)
    i = i + 1
    

# tRot, is the minimum thickness required to achieve the rotational requirement
while True :
    tRot = tRot + 0.00001 
    i = 0
    while i <= 999 :
        J = PMOI.J_calculation(alpha, beta, b[i], DeltaX[i], tRot)
        Jlist.append(J)
        i = i + 1

    rot_lst = RotAngle.rotation(T_lst, Jlist, ylst) * 1/(26*10**9)

    if rot_lst[5] > 0 :
        MaxRot = max(rot_lst)
    else :
        MaxRot = min(rot_lst) * -1
    
    JlistPlot = Jlist 
    Jlist = []
    if MaxRot <= MaxRotReq: 
        break 
    j = j + 1

while True :
    tDef = tDef + 0.000001
    i = 0
    
    while i<= 999:
        Ix_total = MOI.Ixcalculator(DeltaX[i],b[i],alpha,beta,tDef,CG_XList[i],CG_ZList[i])
        Ix_totalList.append(Ix_total) 
        
        if StringersBoolean == True :
            Is_xx, A, s_top, s_bot = Stringer_MOI.moi_stringers(nr_top, nr_bot, L_s, tDef, t_s, alpha, beta, b[i], DeltaX[i])
            Ix_totalList[i] = Ix_totalList[i] + Is_xx

        i = i + 1    
    Def_lst = Deflection.deflection(M_lst, Ix_totalList, ylst) *(1/(68.9*10**9))

    if Def_lst[5] > 0 :
        MaxDef = max(Def_lst)
    else :
        MaxDef = min(Def_lst) * -1

    Ix_totallistPlot = Ix_totalList
    Ix_totalList = []

    if MaxDef <= MaxDefReq :
        break
    k = k + 1


print("Our thickness for torsion is: ", round(tRot, 6), "m")
print("Our thickness for bending is: ", round(tDef, 5), "m")


plt.subplot(211)
plt.plot(ylst ,rot_lst)
plt.title("The rotational angle against the span")
plt.xlabel("The y coordinate of half a wing [m]")
plt.ylabel("The rotational angle [radians] ")


plt.subplot(212)
plt.plot(ylst ,Def_lst)
plt.title("The deflection against the span")
plt.xlabel("The y coordinate of half a wing [m]")
plt.ylabel("The polar moment of inertia [m] ")


plt.show()

