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

tRot= 0.01
tDef = 0.01

MaxRotReq = 5 / 1.5 # This is the max required rotation angle times the safety factor
MaxDefReq = 15 / 1.5 # This is the max required deflection times the safety factor

G = 26*(10**9)     # http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma6061t6
E = 207*(10**9)    # http://asm.matweb.com/search/SpecificMaterial.asp?bassnum=ma6061t6


CG_XList = []
CG_ZList = []
Ix_totalList = []
Iz_totalList = []
ylst = []
T_lst = []
M_lst = []

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

LoadChoice = input(" Which load case do you want to evaluate?\nPos_Crit?(1)\nNeg_crit?(2)")
    

Stringers = input("Are you considering stringers? ('yes' or 'no') ")

if "yes" or "Yes" in Stringers:
    StringersBoolean = False
else:
    StringersBoolean = False
    

if StringersBoolean == True:
    nr_top = int(input("How many stringers are we using at the top? "))
    nr_bot = int(input("How many stringers are we using at the bottem? "))

    if nr_top and nr_bot !=0 :
        L_s = int(input("What is the length of the symetric stringers? "))
        t_s = int(input("What is the thickness of the stringers? "))
        


#---------------------------------------------------------------------------------------------



with open("ylstFRANK.dat", "r") as file : # Reads the y position file 
    ylstRAW = file.readlines()



for line in ylstRAW :
    y = line.replace("\n", "")
    y = float(y)
    #y = round(y, 1)
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
    #T = round(T, 1)
    T_lst.append(T)
    
for line in M_lstRAW :
    M = line.replace("\n", "")
    M = float(M)
    #M = round(M, 1)
    M_lst.append(M)  

del ylstRAW 
del T_lstRAW 
del M_lstRAW 
del T 
del M
del y
del line 
del file


alpha, beta, b, DeltaX, Cr = Lengths.WingboxDimensions(RCr, TCr, Span, ylst) # All geometry is now defined togheter with ylst



del Cr

while (dT * i)<= Span/2 :  # Calculates the CG position in CG_XList 
    CG_x, CG_z = CG.cg_calculation(alpha, beta, b[i], DeltaX[i])
    CG_XList.append(CG_x)
    CG_ZList.append(CG_z)
    i = i + 1
    
del CG_x 
del CG_z 
del CG_ZList

print("Voor ot")
# tRot, is the minimum thickness required to achieve the rotational requierment
while True :
    tRot = tRot + 0.1 
    i = 0
    while i <= 999 :
        J = PMOI.J_calculation(alpha, beta, b[i], DeltaX[i], tRot)
        #J = round(J, 3)
        Jlist.append(J)
        i = i + 1

    del J

    rot_lst = RotAngle.rotation(T_lst, Jlist, 260000, ylst)
    print("4", tRot, MaxRotReq)
    MaxRot = min(rot_lst)
    if MaxRot >= MaxRotReq:
        print("5")
        print(tRot)
        break 
    j = j + 1

print("Rot klaar, nu def")

while True :
    tDef = tDef + 0.001
    i = 0
    while i<= 999:
        Ix_total = MOI.Ixcalculator(DeltaX[i],b[i],alpha,beta,tDef,CG_XList,CG_ZList)
        Ix_totalList.append(Ix_total) 
        i = i + 1

        if StringersBoolean == True :
            Is_xx, A, s_top, s_bot = Stringer_MOI.moi_stringers(nr_top, nr_bot, L_s, tDef, t_s, alpha, beta, b[i], DeltaX[i])
            Ix_totalList[i] = Ix_totalList[i] + Is_xx[I]



    Def_lst = deflection.deflection(M_lst, Ix_totalList, E, ylst)
    MaxDef = max(MaxDef)
    if MaxDef >= MaxDefReq :
        print(tDef)
        break
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











