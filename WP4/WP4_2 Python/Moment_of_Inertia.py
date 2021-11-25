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


#coordinate system: positive z down!!!!!!, positive x right




#inputs (line 1): DeltaX (horizontal distance of wingbox), beta lower profile angle to horizontal axis, alpha upper profile angle to horizontal axis, z position of cg vertically wrt datum

#inputs (line 2): x horizontal position of cg from the datum, b height shorter vertical profile, Ixx_required & Izz_required are obtained from stress calculations



def Ixx(DeltaX,beta,alpha,x,z,b):
    
    Ixx1  =((((DeltaX)**3)*((sin(beta))**2))/(12*((cos(beta))**3)))+((DeltaX)/cos(beta))*(-z+((DeltaX * tan(beta))/2))**2 #lower left angled profile
    
    Ixx2 = ((((DeltaX)**3)*((sin((pi/2)-alpha))**2))/(12*((cos(alpha))**3)))+(DeltaX/(cos(alpha)))*((-DeltaX*tan(beta))-b-((DeltaX*tan(alpha))/2)+z)**2 #upper right angled profile

    Ixx3 = 1/12 * ((DeltaX*tan(beta)+b+DeltaX*tan(alpha))**3) +(DeltaX*tan(beta)+b+DeltaX*tan(alpha))*(z-((DeltaX*tan(beta)+b+DeltaX*tan(alpha))/2))**2 #vertical profile on the left

    Ixx4 = 1/12 * b**3 + b*(DeltaX*tan(beta)+(b/2)-z)**2 #vertical profile on the right

    Ixx = Ixx1 + Ixx2 + Ixx3 + Ixx4

    return Ixx

<<<<<<< HEAD
def Izz(deltax,beta,alpha,x,z,b):


    Izz1 = ((((deltax)**3)*((cos(beta))**2))/(12*((cos(beta))**3)))+((deltax)/cos(beta))*(x-(deltax/2))**2    #lower left angled profile

    Izz2 = ((((deltax)**3)*((cos((pi/2)-alpha))**2))/(12*((cos(alpha))**3)))+(deltax/(cos(alpha)))*(x-(deltax/2))**2   #upper right angled profile
    
    Izz3 = (deltax * tan(beta) + b + deltax * tan(alpha))*x**2  #vertical profile on the left

    Izz4 = b*(deltax-x)**2   #vertical profile on the right

    Izz = Izz1+Izz2+Izz3+Izz4
=======
def Izz(DeltaX,beta,alpha,x,z,b):


    Izz1 = ((((DeltaX)**3)*((cos(beta))**2))/(12*((cos(beta))**3)))+((DeltaX)/cos(beta))*(x-(DeltaX/2))**2    #lower left angled profile

    Izz2 = ((((DeltaX)**3)*((cos((pi/2)-alpha))**2))/(12*((cos(alpha))**3)))+(DeltaX/(cos(alpha)))*(x-(DeltaX/2))**2   #upper right angled profile
    
    Izz3 = (DeltaX * tan(beta) + b + DeltaX * tan(alpha))*x**2  #vertical profile on the left

    Izz4 = b*(DeltaX-x)**2   #vertical profile on the right

    Izz = Izz1 + Izz2 + Izz3 + Izz4
>>>>>>> 4f5ee11e85f771a61d52fb3f5ef75c57e7c24c84

    return Izz


def thickness_selection(Ixx,Izz,Ixx_required,Izz_required):
    

<<<<<<< HEAD
#tx is thickness determined by using Ixx. We will obtain tz from Izz. Whichever is greater is the design thickness as we have to satisfy both cases

    tx = Ixx_required/Ixx
    tz = Izz_required/Izz
=======
#tx is thickness determined by using Ixx. We will obtain ty from Izz. Whichever is greater is the design thickness as we have to satisfy both cases

    tx = Ixx_required/Ixx
    ty = Izz_required/Izz
>>>>>>> 4f5ee11e85f771a61d52fb3f5ef75c57e7c24c84

    t_minimum = max(tx, tz)

    return(t_minimum)

#output: t_minimum is the thinnest the structure should be to barely withstand the loads (chosen as the maximum of tx and tz)



