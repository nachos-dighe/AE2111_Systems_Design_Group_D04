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




































