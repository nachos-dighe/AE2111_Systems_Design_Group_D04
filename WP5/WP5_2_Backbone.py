import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


from math import *

#---------------------------------------------------------------------------------------------
# Import files
import WP5_2_Chord_Length as Length
import WP5_2_stressconcentration as StressCon
import WP5_2_MOI as MOI 
import WP5_2_CG_Wingbox as CG
import WP5_2_min_rho as MinRho


#---------------------------------------------------------------------------------------------

# Geometric
RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 0.1
c = 0.005 # [m]
t = 0.004 #[m]
t_side = 0.00198 # [m]
L_L = 0.01 #[m]
I_c = 0.075 #[m]
I_a = 0.03 #[m]
I_b = 0.075 #[m]
t_L = 0.001
t_I = 0.001

# Material properties
k1c = 29*(10**6) # [Pa]
stress_allow = (276/1.5) *(10**6) #[Pa], tensile


# Counters
i = 0 
j = 0 
k = 0

# Defining lists
y_lst = []
M_lst = []
SafeMar_lst1 = []
SafeMar_lst2 = []

#---------------------------------------------------------------------------------------------
# Reading files to get the spanwise coordinates and bending loads

LoadChoice = input("Which load case do you want to evaluate?\nPos_Crit?(1)\nNeg_crit?(2)")
DesignChoice = input("Which design choice do you want to evaluate?\nDesign 1\nDesign 2\nDesign3")

with open("ylst.dat", "r") as file : # Reads the y position file 
    ylstRAW = file.readlines()

for line in ylstRAW :
    y = line.replace("\n", "")
    y = float(y)
    y_lst.append(y)

if "1" in LoadChoice:
    with open("Critical_Load_Bending_Pos_Crit.dat", "r") as file : 
        M_lstRAW = file.readlines()

elif "2" in LoadChoice:
    with open("Critical_Load_Bending_Neg_Crit.dat", "r") as file : 
        M_lstRAW = file.readlines()

else :
    print("Answer either '1' or '2' for choice. Please restart the code to work!")
    
for line in M_lstRAW :
    M = line.replace("\n", "")
    M = float(M)
    M_lst.append(M)
# Output, y_lst, M_lst

#---------------------------------------------------------------------------------------------
# Main code

#Wingbox dimension lists
alpha, beta, b, DeltaX, Cr = Length.WingboxDimensions(RCr, TCr, Span, y_lst)

#obtain minimal rho satisfying minimum safety factor of 1
min_rho = MinRho.min_rho(c, k1c, M_lst, alpha, beta, b, DeltaX, Cr, t)

print(min_rho)
#min_rho = 0.006 #the min rho most limiting neg/pos case

#iterate per data point in spanwise direction
for i in range(0,300):
    CG_X, CG_Z = CG.cg_calculation (alpha, beta, b[i], DeltaX[i])

    if DesignChoice == 1:
        number_of_I_stringers_top = 2
        number_of_I_stringers_bottom = 2
    if DesignChoice == 2:
        number_of_I_stringers_top = 3
        number_of_I_stringers_bottom = 2
    if DesignChoice == 3:
        number_of_I_stringers_top = 3
        number_of_I_stringers_bottom = 3
    maxstres1, maxstress2, maxstress2 = MOI.normal_stress_calculator(CG_X,CG_Z,alpha,beta[i],DeltaX[i],b,t_side, t,L_L,t_L,I_c,I_a,I_b,t_I,number_of_I_stringers_top,number_of_I_stringers_bottom,A_L,abs(M_lst[i]))
    #stress_nom = MOI.normal_stress (Ixx,Ixz,Izz,CG_Z,CG_X,abs(M_lst[i]), DeltaX[i], beta) #update to sress1, stess2, stress3 = call function
    if DesignChoice == 1:
        stress_nom = maxstress1
    if DesignChoice == 2:
        stress_nom = maxstress2
    if DesignChoice == 3:
        stress_nom = maxstress3
    safety_margin = StressCon.safety(c, min_rho, k1c, stress_nom)
    SafeMar_lst1.append(safety_margin)
    safety_margin2 = stress_allow / stress_nom
    SafeMar_lst2.append(safety_margin2)

#---------------------------------------------------------------------------------------------
# Graphs
y_lst_plt = []

for i in range(0,300):
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

#lower rho higher safety stress constr => lower safety margin
#higher rho is better, so low is more critical


#Manual to complete it once the moment of inertia's are finalised
#Run the code per design for the positive as well as the negative load case
#Check what is the higher min rho, then take that as the rho to calculate the final safety margin graphs for that design
#Iterate this for all 3 designs, clearly state what the min rho's are per design

#Make the plots and put them in overleaf
#Talk per plot about how the safetymargin should stay above 1 for both loading cases of each design

#In the end re-upload the code files to overleaf to have the up to date files in there




























