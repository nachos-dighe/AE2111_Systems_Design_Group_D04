import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


from math import *

#---------------------------------------------------------------------------------------------
# Import files
import WP5_2_Chord_Length as Length
import WP5_2_stressconcentration as StressCon
import WP5_2_MOI_trial as MOI #needs to be changed when done
import WP5_2_CG_Wingbox as CG
import WP5_2_min_rho as MinRho


#---------------------------------------------------------------------------------------------

# Geometric
RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 0.1
c = 0.005 # [m]
t = 0.00198 #[m]

# Material properties
k1c = 29*(10**6) # [Pa]
stress_allow = (276/1.5) *(10**6) #[Pa], tensile


# Counters
i = 0 
j = 0 
k = 0

# Defining lists
y_lst = []
T_lst = []
M_lst = []
rhodiff_lst = []
SafeMar_lst1 = []
SafeMar_lst2 = []
SafeMar_lst3 = []


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

#obtain minimal rho satisfying minimum safety factor of 1.5
min_rho = MinRho.min_rho(c, k1c, M_lst, alpha, beta, b, DeltaX, Cr, t)
min_rho = 0.052 #the min rho most limiting neg/pos case
#min_rho not final bc mom of I is not final

#iterate per data point in spanwise direction
for i in range(0,1000):
    CG_X, CG_Z = CG.cg_calculation (alpha, beta, b[i], DeltaX[i])
    Ixx = MOI.Ixx_wingbox (DeltaX[i],beta,alpha,CG_Z,t,b[i])
    Ixz = MOI.Ixz_wingbox(DeltaX[i],beta,alpha,CG_X,CG_Z,t,b[i])
    Izz = MOI.Izz_wingbox(DeltaX[i],beta,alpha,CG_X,t,b[i])
    stress_nom = MOI.normal_stress (Ixx,Ixz,Izz,CG_Z,CG_X,abs(M_lst[i]), DeltaX[i], beta)
    safety_margin = StressCon.safety(c, min_rho, k1c, stress_nom)
    SafeMar_lst1.append(safety_margin)
    safety_margin2 = stress_allow / stress_nom
    SafeMar_lst2.append(safety_margin2)
    

#---------------------------------------------------------------------------------------------
# Graphs
y_lst_plt = []

for i in range(0,1000):
    y = y_lst[i]
    y_lst_plt.append(y)
    

plt.plot(y_lst_plt , SafeMar_lst1, label="Crack propagation")
plt.plot(y_lst_plt , SafeMar_lst2, label="Tensile yield strength")
plt.title("Saftey margin")
plt.xlabel("The y coordinate of half a wing [m]")
plt.ylabel("")
plt.grid()
plt.legend(loc='best')
plt.show()



#the negative case can withstand rho of 2 mm
#the positive 0.052 so 52 mm
#

#lower rho higher safety stress constr => lower safety margin
#higher rho is better, so low is more critical































