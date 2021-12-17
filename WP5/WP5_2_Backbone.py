import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


from math import *
1
#---------------------------------------------------------------------------------------------
# Import files
import WP5_2_Chord_Length as Length
import WP5_2_stressconcentration as StressCon
import WP5_2_MOI as MOI 
import WP5_2_CG_Wingbox as CG
import WP5_2_min_rho as MinRho


#---------------------------------------------------------------------------------------------

# Geometric
RCr = 4.4           #[m] Root chord
TCr = 1.76          #[m] Tip chord
Span = 24.64        #[m] Span
dT = 0.1            #[Nm]
c = 0.005           #[m]
t = 0.004           #[m]
t_side = 0.004    #[m]
L_L = 0.01          #[m]
I_c = 0.075         #[m]
I_a = 0.03          #[m]
I_b = 0.075         #[m]
t_L = 0.001         #[m]
t_I = 0.001         #[m]
A_L = 300 * (10**-6)#[m]


# Material properties
k1c = 29*(10**6) # [Pa], fracture toughness
stress_allow = (276/1.5) *(10**6) #[Pa], tensile yield stress

# Defining lists
y_lst = []
M_lst = []
SafeMar_lst1 = []
SafeMar_lst2 = []

#---------------------------------------------------------------------------------------------
# Reading files to get the spanwise coordinates and bending loads

LoadChoice = input("Which load case do you want to evaluate?\nPos_Crit?(1)\nNeg_crit?(2)")
DesignChoice = input("Which design choice do you want to evaluate?\nDesign 1\nDesign 2\nDesign 3")

with open("ylst.dat", "r") as file :
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
min_rho = MinRho.min_rho(c, k1c, M_lst, alpha, beta, b, DeltaX, Cr, t, DesignChoice,t_side,L_L,t_L,I_c,I_a,I_b,t_I,A_L)

print(min_rho)

#min_rho = 0.172 #the min rho most limiting neg/pos case design 1
#min_rho = 0.167  #the min rho most limiting neg/pos case design 2
#min_rho = 0.163  #the min rho most limiting neg/pos case design 2

#iterate per data point in spanwise direction
for i in range(0,325):
    CG_X, CG_Z = CG.cg_calculation (alpha, beta, b[i], DeltaX[i])
 
    maxstress1, maxstress2, maxstress3 = MOI.normal_stress_calculator(CG_X,CG_Z,alpha,beta,DeltaX[i],b[i],t_side, t,L_L,t_L,I_c,I_a,I_b,t_I,A_L,abs(M_lst[i]))
    if "1" in DesignChoice:
        stress_nom = maxstress1
    if "2" in DesignChoice:
        stress_nom = maxstress2
    if "3" in DesignChoice:
        stress_nom = maxstress3
    safety_margin = StressCon.safety(c, min_rho, k1c, stress_nom)
    SafeMar_lst1.append(safety_margin)
    safety_margin2 = stress_allow / stress_nom
    SafeMar_lst2.append(safety_margin2)

#---------------------------------------------------------------------------------------------
# Graphs
y_lst_plt = []

for i in range(0,325):
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























