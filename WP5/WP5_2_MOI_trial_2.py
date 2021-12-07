import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate
from math import tan
from math import sin
from math import cos
from math import pi
import math

#1. Ixx Ixz Izz formula for wingbox (Done)
#2. Ixx Ixz Izz local of stringers chosen 
#3. Design type specific total Ixx Ixz Izz (step 1 + design specific stringer configuration)
#4. Stress calculator at extreme points for tension for each design


import CG_wingboxFRANK as CG
import WP5_2_Chord_Length as ChordLength


stress = []

t = 1.98 * 10**(-3)

#inputs: all dimensions of the wingbox including angle and CG location, dimensions of the stringers and their position wrt datum point, moment along the span

#coordinate system: positive z down, positive x right

#VERY IMPORTANT: CG_X VALUE IS +, CG_Z VALUE IS NEGATIVE (from the output of cg calculator)


def Ixx_wingbox(DeltaX,beta,alpha,CG_Z,t):
    
    Ixx1  =((t*((DeltaX)**3)*((sin(beta))**2))/(12*((cos(beta))**3)))+((t*DeltaX)/cos(beta))*(-CG_Z+((DeltaX * tan(beta))/2))**2 #lower left angled profile
    
    Ixx2 = (t*((DeltaX)**3)*((sin((alpha))**2))/(12*((cos(alpha))**3)))+(t*DeltaX/(cos(alpha)))*((-DeltaX*tan(beta))-b-((DeltaX*tan(alpha))/2)+CG_Z)**2 #upper right angled profile

    Ixx3 = (1/12) * t*((DeltaX*tan(beta)+b+DeltaX*tan(alpha))**3) +t*(DeltaX*tan(beta)+b+DeltaX*tan(alpha))*(CG_Z-((DeltaX*tan(beta)+b+DeltaX*tan(alpha))/2))**2 #vertical profile on the left

    Ixx4 = (1/12) * t * b**3 + b*t*(DeltaX*tan(beta)+(b/2)-CG_Z)**2 #vertical profile on the right

    Ixx_wingbox = Ixx1 + Ixx2 + Ixx3 + Ixx4

    return  Ixx_wingbox



def Izz_wingbox(DeltaX,beta,alpha,CG_X,t):

    Izz1 = ((t*((DeltaX)**3)*((cos(beta))**2))/(12*((cos(beta))**3)))+(t*(DeltaX)/cos(beta))*(CG_X-(DeltaX/2))**2    #lower left angled profile

    Izz2 = ((t*(DeltaX)**3)*((cos((alpha))**2))/(12*((cos(alpha))**3)))+(t*DeltaX/(cos(alpha)))*(CG_X-(DeltaX/2))**2   #upper right angled profile

    Izz3 = t*(DeltaX * tan(beta) + b + DeltaX * tan(alpha))*((CG_X)**2)  #vertical profile on the left

    Izz4 = t*b*((DeltaX-CG_X)**2)   #vertical profile on the right

    Izz_wingbox = Izz1 + Izz2 + Izz3 + Izz4

    return Izz_wingbox



def Ixz_wingbox(DeltaX,beta,alpha,CG_X,CG_Z,t): 

    #check all x and y position for all Ixz

    Ixz1 = (1/12) * t * (DeltaX/cos(beta))**3 * sin(beta) * cos(beta) + (DeltaX/cos(beta)) * t * ((DeltaX/2)-CG_X) * (-CG_Z-((DeltaX * tan(beta))/2)) #lower left angled profile (+x)*(+z)

    Ixz2 = (1/12) * t * (DeltaX/cos(alpha))**3 * sin(alpha) * cos(alpha) + (DeltaX/cos(alpha))*t*((DeltaX/2)-CG_X)*(-b-DeltaX *tan(beta)-((DeltaX*tan(alpha))/2)-CG_z) #upper right angled profile (+x)*(-z)

    Ixz3 = (DeltaX*tan(beta)+b+DeltaX*tan(alpha))*t*(-CG_X) * (-CG_Z - (DeltaX * tan(alpha) + b + DeltaX * tan (beta))/2)  #vertical profile on the left (-x)*(+z)

    Ixz4 = b * t * (DeltaX - CG_X) * (-CG_Z -((b+DeltaX * tan(beta))/2))  #vertical profile on the right (+x)*(+z)

    Ixz_wingbox = Ixz1 + Ixz2 + Ixz3 + Ixz4

    return Ixz_wingbox
    
# Defining lists
y_lst = []
T_lst = []
M_lst = []

#SafeMar_lst = []


#---------------------------------------------------------------------------------------------
#Reading files to get the spanwise coordinates, bending loads and torisonal loads

LoadChoice = input("Which load case do you want to evaluate?\nPos_Crit?(1)\nNeg_crit?(2)")

with open("ylst.dat", "r") as file : # Reads the y position file 
    y_lstRAW = file.readlines()

for line in y_lstRAW :
    #y = line.replace("\n", "")
    #y = float(y)
    #y_lst.append(y)


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

    
############################################################################################################################################################################################


#def Ixx_L_stringer(blah, blah, blah):

    #return Ixx_L_stringer

#def Izz_L_stringer(blah,blah,blah):


    #return Izz_L_stringer


#def Ixz_L_stringer(blah,blah,blah):

    #return Ixz_L_stringer


#def Ixx_something_stringer(...):




#def Izz_something_stringer(...):



#def Ixz_something_stringer(...):


############################################################################################################################################################################################


#design 1: 4 L stringers, all on the corners
    
#def design_1_max_stress(Ixx_wingbox, Ixz_wingbox, Izz_wingbox, Ixx_L_stringer, Izz_L_stringer, Ixz_L_stringer):
    
    #Ixx_design_1 = Ixx_wingbox + 2 * (Ixx_L_stringer + area * distance_above**2) + 2 * (Ixx_L_striger + area * distance_below**2)
                                                                                    
    #Izz_design_1 =

    #Ixz_design_1 =

    #max_tensile_Stress_1 = (M_x * Izz_design_1 * (-CG_Z) + M_x * Ixz_design_1 * (-CG_X))/(Ixx_design_1*Izz_design_1 -((Ixz_design_1)**2))

    #max_tensile_Stress_2 = (M_x * Izz_design_1 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_1 * (DetlaX-CG_X))/(Ixx_design_1*Izz_design_1-((Ixz_design_1)**2))

    #max_tensile_Stress_design_1 = max(max_tensile_Stress_1,max_tensile_Stress_2)

    #return max_tensile_design_1

#design 2: 4 L stringers all on the corners  + 1 stringer placed exactly at the middle of the top face (Shape TBD)


#def design_2_max_stress(Ixx_wingbox, Ixz_wingbox, Izz_wingbox, Ixx_L_stringer, Izz_L_stringer, Ixz_L_stringer): #change when stringers chosen
    
    #Ixx_design_2 = Ixx_wingbox + 2 * (Ixx_L_stringer + area * distance_above**2) + 2 * (Ixx_L_striger + area * distance_below**2)
                                                                                    
    #Izz_design_2 =

    #Ixz_design_2 = 

    #max_tensile_Stress_1 = (M_x * Izz_design_2 * (-CG_Z) + M_x * Ixz_design_2 * (-CG_X))/(Ixx_design_2*Izz_design_2 -((Ixz_design_2)**2))

    #max_tensile_Stress_2 = (M_x * Izz_design_2 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_2 * (DetlaX-CG_X))/(Ixx_design_2*Izz_design_2-((Ixz_design_2)**2))

    #max_tensile_Stress_design_2 = max(max_tensile_Stress_1,max_tensile_Stress_2)

    #return max_tensile_design_2

#design 3: 4 L stringers all on the corners + 1 stringer placed exactly at the middle of the top face (Shape TBD) + 1 stringer placed exactly at the middle of the lower face (Shape TBD)


#def design_3_max_stress(Ixx_wingbox, Ixz_wingbox, Izz_wingbox, Ixx_L_stringer, Izz_L_stringer, Ixz_L_stringer): #change when stringers chosen
    
    #Ixx_design_3 = Ixx_wingbox + 2 * (Ixx_L_stringer + area * distance_above**2) + 2 * (Ixx_L_striger + area * distance_below**2)
                                                                                    
    #Izz_design_3 = 

    #Ixz_design_3 =

    #max_tensile_Stress_1 = (M_x * Izz_design_1 * (-CG_Z) + M_x * Ixz_design_1 * (-CG_X))/(Ixx_design_1*Izz_design_1 -((Ixz_design_1)**2))

    #max_tensile_Stress_2 = (M_x * Izz_design_1 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_1 * (DetlaX-CG_X))/(Ixx_design_1*Izz_design_1-((Ixz_design_1)**2))

    #max_tensile_Stress_design_3 = max(max_tensile_Stress_1,max_tensile_Stress_2)

    #return max_tensile_design_3


#max_tensile_stress.append(max_tensile_design_1,max_tensile_design_2, max_tensile_design_3)


    

    #return Ixx_design_1, Izz_design_1, Ixz_design_1


def stress_calculator(Ixx_wingbox,Ixz_wingbox,Izz_wingbox,CG_Z,CG_X,M_x,DeltaX,beta):
    
    max_tensile_Stress_1 = (M_x * Izz_wingbox * (-CG_Z) + M_x * Ixz_wingbox * (-CG_X))/(Ixx_wingbox*Izz_wingbox-((Ixz_wingbox)**2))

    max_tensile_Stress_2 = (M_x * Izz_wingbox * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_wingbox * (DetlaX-CG_X))/(Ixx_wingbox*Izz_wingbox-((Ixz_wingbox)**2))

    max_tensile_Stress = max(max_tensile_Stress_1,max_tensile_Stress_2)

    return max_tensile_stress




RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 5
i = 0





alpha, beta, b, DeltaX, Cr  = ChordLength.WingboxDimensions(RCr, TCr, Span, y_lst)


while i <= len(y_lst) :
  CG_X, CG_Z = CG.cg_calculation(alpha, beta, b[i], DeltaX[i])
  i = i +1

i = 0


while i <= len(y_lst):
    Ixx_wingbox = Ixx_wingbox(DeltaX[i],beta,alpha,CG_Z[i],t)
    i= i + 1

i = 0
while i <= len(y_lst):
    Izz_wingbox = Izz_wingbox(DeltaX[i],beta,alpha,CG_X[i],t)
    i= i + 1

i = 0

while i <= len(y_lst):
    Ixz_wingbox = Ixz_wingbox(DeltaX[i],beta,alpha,CG_X[i],CG_Z[i],t)
    i= i + 1

i = 0


while i <= len(y_lst) :
    max_tensile_stress = stress_calculator(Ixx_wingbox[i],Ixz_wingbox[i],Izz_wingbox,CG_Z[i],CG_X[i],M_x[i],DeltaX[i],beta)
    i = i + 1

    stress.append(max_tensile_stress)

print(stress)



    
#def normal_stress(Ixx,Ixz,Izz,CG_Z,CG_X,M_x):


        #sigma_y = (M_x * Izz * z + M_x * Ixz * x)/(Ixx*Izz-((Ixz)**2))

        #we thing that the sign between the two terms in the numerator is + but from normal stress equation is should be -.
        #We think it should be + since we defined x + right, in formula sheet its defined x + left.

        # 2 critical positions for max tension (bottom left or bottom right)

       # max_tensile_Stress_1 = (M_x * Izz * (-CG_Z) + M_x * Ixz * (-CG_X))/(Ixx*Izz-((Ixz)**2))

       # max_tensile_Stress_2 = (M_x * Izz * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz * (DetlaX-CG_X))/(Ixx*Izz-((Ixz)**2))

       # max_tensile_Stress = max(max_tensile_Stress_1,max_tensile_Stress_2)

      #  return max_tensile_stress

        

        

    

   
    





