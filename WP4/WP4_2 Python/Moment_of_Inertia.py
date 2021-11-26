import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

from math import tan
from math import sin
from math import cos
from math import pi
import math


#Angles in radians!!!


#coordinate system: positive z down, positive x right


#inputs (line 1): DeltaX (horizontal distance of wingbox), beta lower profile angle to horizontal axis, alpha upper profile angle to horizontal axis, 

#inputs (line 2): z position of cg vertically wrt datum, b height shorter vertical profile, Ixx_required is obtained from max deflection calculation


#Note: all of the section Ixx formulas are written without thickness as t will move to the opposite side of the equation when total Ixx is divided from Ixx_required
def thickness_calculator(DeltaX,beta,alpha,z,b,Ixx_required):
    
    Ixx1  =((((DeltaX)**3)*((sin(beta))**2))/(12*((cos(beta))**3)))+((DeltaX)/cos(beta))*(-z+((DeltaX * tan(beta))/2))**2 #lower left angled profile
    
    Ixx2 = (((DeltaX)**3)*((sin((alpha))**2))/(12*((cos(alpha))**3)))+(DeltaX/(cos(alpha)))*((-DeltaX*tan(beta))-b-((DeltaX*tan(alpha))/2)+z)**2 #upper right angled profile

    Ixx3 = 1/12 * ((DeltaX*tan(beta)+b+DeltaX*tan(alpha))**3) +(DeltaX*tan(beta)+b+DeltaX*tan(alpha))*(z-((DeltaX*tan(beta)+b+DeltaX*tan(alpha))/2))**2 #vertical profile on the left

    Ixx4 = 1/12 * b**3 + b*(DeltaX*tan(beta)+(b/2)-z)**2 #vertical profile on the right

    Ixx_without_stringers = Ixx1 + Ixx2 + Ixx3 + Ixx4

    t_minimum_without_stringers = Ixx_required/Ixx_without_stringers 

    return t_minimum_without_stringers , Ixx_without_stringers

    

#output 1: t_minimum_without_stringers is the thinnest the structure should be to just satisfy the deflection requirement when wingbox does not have stringers attached
#output 2: MOI of structure without additional MOI of stringers



