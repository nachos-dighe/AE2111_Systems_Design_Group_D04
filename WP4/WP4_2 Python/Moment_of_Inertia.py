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




#inputs (line 1): deltax (horizontal distance of wingbox), beta lower profile angle to horizontal axis, alpha upper profile angle to horizontal axis, z position of cg vertically wrt datum

#inputs (line 2): x horizontal position of cg from the datum, b height shorter vertical profile, Ixx & Iyy obtained from stress calculations




Ixx1  =((((deltax)**3)*((sin(beta))**2))/(12*((cos(beta))**3)))+((deltax)/cos(beta))*(-z+((deltax * tan(beta))/2))**2 #lower left angled profile
    
Ixx2 = ((((deltax)**3)*((sin((pi/2)-alpha))**2))/(12*((cos(alpha))**3)))+(deltax/(cos(alpha)))*((-deltax*tan(beta))-b-((deltax*tan(alpha))/2)+z)**2 #upper right angled profile

Ixx3 = 1/12 * ((deltax*tan(beta)+b+deltax*tan(alpha))**3) +(deltax*tan(beta)+b+deltax*tan(alpha))*(z-((deltax*tan(beta)+b+deltax*tan(alpha))/2))**2 #vertical profile on the left

Ixx4 = 1/12 * b**3 + b*(deltax*tan(beta)+(b/2)-z)**2 #vertical profile on the right



Iyy1 = ((((deltax)**3)*((cos(beta))**2))/(12*((cos(beta))**3)))+((deltax)/cos(beta))*(x-(deltax/2))**2    #lower left angled profile

Iyy2 = ((((deltax)**3)*((cos((pi/2)-alpha))**2))/(12*((cos(alpha))**3)))+(deltax/(cos(alpha)))*(x-(deltax/2))**2   #upper right angled profile

Iyy3 = (deltax * tan(beta) + b + deltax * tan(alpha))*x**2  #vertical profile on the left

Iyy4 = b*(deltax-x)**2   #vertical profile on the right
    

#tx is thickness determined by using Ixx. We will obtain ty from Iyy. Whichever is greater is the design thickness as we have to satisfy both cases

tx = Ixx/(Ixx1+Ixx2+Ixx3+Ixx4)
ty = Iyy/(Iyy1+Iyy2+Iyy3+Iyy4)

t_minimum = max(tx, ty)

#output: t_minimum is the thinnest the structure should be to barely withstand the loads (chosen as the maximum of tx and ty)



