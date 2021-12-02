import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


from math import *

#---------------------------------------------------------------------------------------------
# Import files
import WP5_2_stressconcentration as StressCon


#---------------------------------------------------------------------------------------------

# Geometric
RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 0.1
c = 0.005 # [m]
k1c = 29*(10**6) # [Pa]



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

#defining rho, checking influence
rho = 0.001
while True:
    safety_margin1 = StressCon(0.005, rho, 29*(10**6), stress_mom)
    rho = rho + 0.001
    safety_margin2 = StressCon (0.005, rho, 29*(10**6), stress_mom)
    difference = ((safety_margin2 - safety_margin1)/safety_margin1)*100
    if difference <= 1:
        break

#now the rho is used after which it has negl. influence on the safety margin
stress_max = (1 + 2*((c/rho)**0.5))*stress_nom
fail_stress = k1c/((pi * c)**0.5)
safety_margin = prop_stress/stress_max

#check if safety_margin is bigger than 1.5
while True:
    if safety_margin <= 1.5:
        break
    rho = rho - 0.001
    safety_margin = StressCon (0.005, rho, 29*(10**6), stress_mom)
    if rho <= 0:
        print("The 1.5 safety margin is never reached for any rho, the moment of inertia should be re-evaluated")
        break







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




































