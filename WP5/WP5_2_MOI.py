import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

from math import tan
from math import sin
from math import cos
from math import pi
import math


t = 1.98 * 10**(-3)

#coordinate system: positive z down, positive x right


def Ixx_wingbox(DeltaX,beta,alpha,CG_Z,t):
    
    Ixx1  =((t*((DeltaX)**3)*((sin(beta))**2))/(12*((cos(beta))**3)))+((t*DeltaX)/cos(beta))*(-CG_Z+((DeltaX * tan(beta))/2))**2 #lower left angled profile
    
    Ixx2 = (t*((DeltaX)**3)*((sin((alpha))**2))/(12*((cos(alpha))**3)))+(t*DeltaX/(cos(alpha)))*((-DeltaX*tan(beta))-b-((DeltaX*tan(alpha))/2)+CG_Z)**2 #upper right angled profile

    Ixx3 = 1/12 * t*((DeltaX*tan(beta)+b+DeltaX*tan(alpha))**3) +t*(DeltaX*tan(beta)+b+DeltaX*tan(alpha))*(CG_Z-((DeltaX*tan(beta)+b+DeltaX*tan(alpha))/2))**2 #vertical profile on the left

    Ixx4 = 1/12 * t * b**3 + b*t*(DeltaX*tan(beta)+(b/2)-CG_Z)**2 #vertical profile on the right

    Ixx_wingbox = Ixx1 + Ixx2 + Ixx3 + Ixx4

    return  Ixx_wingbox



#def Ixx_stringer....





def Izz_wingbox(DeltaX,beta,alpha,CG_X,t):

    Izz1 = ((t*((deltax)**3)*((cos(beta))**2))/(12*((cos(beta))**3)))+(t*(deltax)/cos(beta))*(CG_X-(deltax/2))**2    #lower left angled profile

    Izz2 = (((t*(deltax)**3)*((cos((alpha))**2))/(12*((cos(alpha))**3)))+(t*deltax/(cos(alpha)))*(CG_X-(deltax/2))**2   #upper right angled profile

    Izz3 = t*(deltax * tan(beta) + b + deltax * tan(alpha))*CG_X**2  #vertical profile on the left

    Izz4 = t*b*(deltax-CG_X)**2   #vertical profile on the right

    Izz_wingbox = Izz1 + Izz2 + Izz3 + Izz4

    return Izz_wingbox

#def Iyy_stringer....




def Ixz_wingbox(DeltaX,beta,alpha,CG_X,CG_Z,t): #CHECK AGAIN FOR POSITIONS

    #check all x and y position for all Ixz

    Ixz1 = 1/12 * t * (DeltaX/cos(beta))**3 * sin(beta) * cos(beta) + (DeltaX/cos(beta)) * t * ((DeltaX/2)-CG_X) * (-CG_Z+((DeltaX * tan(beta))/2))) #lower left angled profile

    Ixz2 = 1/12 * t * (DeltaX/cos(alpha))**3 * sin(alpha) * cos(alpha) + (DeltaX/cos(alpha))*t*((DeltaX/2)-CG_X)*(-b-DeltaX *tan(beta)-((DeltaX*tan(alpha))/2)-CG_z) #upper right angled profile

    Ixz3 = (DeltaX*tan(beta)+b+DeltaX*tan(alpha))*t*(-CG_X) * (-CG_Z + (DeltaX * tan(alpha) + b + DeltaX * tan (beta))/2)  #vertical profile on the left

    Ixz4 = b * t * (DeltaX - CG_X) * (-CG_z+((b+DeltaX * tan(beta))/2)))  #vertical profile on the right

    Ixz_wingbox = Ixz1 + Ixz2 + Ixz3 + Ixz4

    return Ixz_wingbox
    


#def Ixz_stringers...

    



def Ixx_total(Ixx_wingbox,Ixx_stringer,n): #n number of stringers but recheck it probably incorrect interpretation

    Ixx = Ixx_wingbox + n * Ixx_stringers

    return Ixx




def Izz_total(Izz_wingbox,Izz_stringer,n): #n number of stringers but recheck it probably incorrect interpretation

    Izz = Izz_wingbox + n * Izz_stringer

    return Izz




def Ixz_total(Ixz_wingbox, Ixz_stringers,n): #n number of stringers but recheck it probably incorrect interpretation

    Ixz = Ixz_wingbox + n * Izz_stringer


    return Ixz






def normal_stress(Ixx,Ixz,Izz,x,z,M_x,y):


        sigma_y = (M_x * Izz * z + M_x * Ixz * x)/(Ixx*Izz-((Ixz)**2))

         #we thing that the sign between the two terms in the numerator is + but from normal stress equation is should be -.
        #We think it should be + since we defined x + right, in formula sheet its defined x + left.

        # 2 critical positions for max tension (bottom left or bottom right)

        max_tensile_Stress_1 = (M_x * Izz * CG_Z + M_x * Ixz * (-CG_x))/(Ixx*Izz-((Ixz)**2))

        max_tensile_Stress_2 = (M_x * Izz * (CG_Z-DeltaX*tan(beta)) + M_x * Ixz * (DetlaX-CG_X))/(Ixx*Izz-((Ixz)**2))

        max_tensile_Stress = max(max_tensile_Stress_1,max_tensile_Stress_2)

        return max_tensile_stress

        

        

    

   
    





