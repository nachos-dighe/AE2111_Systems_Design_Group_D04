import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


from math import *

#---------------------------------------------------------------------------------------------
# Import files
import WP5_2_Chord_Length as Length
import WP5_2_stressconcentration as StressCon
import MOI_trial as MOI
import WP5_2_CG_Wingbox as CG


#---------------------------------------------------------------------------------------------

# Geometric
RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 0.1
c = 0.005 # [m]
k1c = 29*(10**6) # [Pa]
t = 0.00198 #[m]



# Material properties


# Counters
i = 0 
j = 0 
k = 0

# Defining lists
y_lst = []
T_lst = []
M_lst = []

SafeMar_lst = []


#---------------------------------------------------------------------------------------------
# Reading files to get the spanwise coordinates, bending loads and torisonal loads

LoadChoice = input("Which load case do you want to evaluate?\nPos_Crit?(1)\nNeg_crit?(2)")

with open("ylst.dat", "r") as file : # Reads the y position file 
    ylstRAW = file.readlines()

for line in ylstRAW :
    y = line.replace("\n", "")
    y = float(y)
    y_lst.append(y)


if "1" in LoadChoice:
    with open("Critical_Load_Torsion_Pos_Crit.dat", "r") as file : 
        T_lstRAW = file.readlines()
    with open("Critical_Load_Bending_Pos_Crit.dat", "r") as file : 
        M_lstRAW = file.readlines()

elif "2" in LoadChoice:
    with open("Critical_Load_Torsion_Neg_Crit.dat", "r") as file : 
        T_lstRAW = file.readlines()
    with open("Critical_Load_Bending_Neg_Crit.dat", "r") as file : 
        M_lstRAW = file.readlines()

else :
    print("Answer either '1' or '2' for choice. Please restart the code to work!")

for line in T_lstRAW :
    T = line.replace("\n", "")
    T = float(T)
    T_lst.append(T)
    
for line in M_lstRAW :
    M = line.replace("\n", "")
    M = float(M)
    M_lst.append(M)


# Output, y_lst, M_lst, T_lst
#---------------------------------------------------------------------------------------------
# Main code

#Wingbox dimension lists
alpha, beta, b, DeltaX, Cr = Length.WingboxDimensions(RCr, TCr, Span, y_lst)

#iterate per data point in spanwise direction
for i in range(0,len(y_lst)):
    #obtaining the max bending stress in the cross section
    CG_X, CG_Z = CG.cg_calculation (alpha, beta, b[i], DeltaX[i])
    Ixx = MOI.Ixx_wingbox (DeltaX[i],beta,alpha,CG_Z,t,b[i])
    Ixz = MOI.Ixz_wingbox(DeltaX[i],beta,alpha,CG_X,CG_Z,t,b[i])
    Izz = MOI.Izz_wingbox(DeltaX[i],beta,alpha,CG_X,t,b[i])
    M_x = M_lst[i]
    stress_nom = MOI.normal_stress (Ixx,Ixz,Izz,CG_Z,CG_X,M_lst[i], DeltaX[i], beta)
    
    #defining rho, checking influence
    rho = 0.001
    while True:
        safety_margin1 = StressCon.safety(c, rho, k1c, stress_nom)
        rho = rho + 0.001
        safety_margin2 = StressCon.safety(c, rho, k1c, stress_nom)
        difference = ((safety_margin2 - safety_margin1)/safety_margin1)*100
        if difference <= 1:
            break

    #now the rho is used after which it has negl. influence on the safety margin
    
    safety_margin = StressCon.safety(c, rho, k1c, stress_nom)
    SafeMar_lst.append(safety_margin)
    
#check if safety_margin is bigger than 1.5
exceed_lst = []
for j in range(0,1000):
    if SafeMar_lst[j] <= 1.5:
        exceed_lst.append(j)
#if len(exceed_lst)
#    while True:
 #       if safety_margin >= 1.5:
  #          
   #         break
    #    rho = rho - 0.001
     #   safety_margin = StressCon.safety (c, rho, k1c, stress_nom)
      #  if rho <= 0.001:
       #     j = j +1            
        #    break

#if j >= 1:
 #   print("The 1.5 safety margin is never reached for any rho, the moment of inertia should be re-evaluated")

print(exceed_lst)



# Output (for graphs to work) SafeMar_lst
#---------------------------------------------------------------------------------------------
# Graphs

##plt.subplot(211)
##plt.plot(ylst ,SafeMar_lst)
##plt.title("Saftey margin")
##plt.xlabel("The y coordinate of half a wing [m]")
##plt.ylabel("")
##
##
##plt.subplot(212)
##plt.plot(ylst ,SafeMar_lst)
##plt.title("The deflection against the span")
##plt.xlabel("The y coordinate of half a wing [m]")
##plt.ylabel("")




































