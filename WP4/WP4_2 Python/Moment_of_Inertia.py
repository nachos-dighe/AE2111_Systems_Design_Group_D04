import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

from math import tan
import math


#Angles in radians!!!



#coordinate system: positive z up, positive x right

def Ixcalculator(deltax,b,alpha,beta,t,x,z):
    
    Ix_rectangle_outer = (1/12)* deltax * (b**3) + deltax * b * (z - (deltax*tan(beta)+(b/2)))**2 
    
    Ix_upper_triangle_outer = (1/36) * deltax * ((deltax* tan(alpha))**3) + ((deltax*deltax*tan(alpha))/2)*(deltax*tan(beta)+b+(1/3)*deltax*tan(alpha)-z)**2

    Ix_lower_triangle_outer = (1/36) * deltax * ((deltax* tan(beta))**3) + ((deltax*deltax*tan(beta))/2)*(z-((2/3)*deltax*tan(beta)))**2 

    Ix_rectangle_inner = (1/12)*(deltax-2*t)*((b-2*t)**3)+(deltax-2*t)*(b-2*t)*(z-(t+(deltax-2*t)*tan(beta)+((b-2*t)/2)))**2 

    Ix_upper_triangle_inner = (1/36) * (deltax-2*t)*(((deltax-2*t)*tan(alpha))**3)+(((deltax-2*t)*(deltax-2*t)*tan(alpha))/2)*(t+(deltax-2*t)*tan(beta)+(b-2*t)+(((deltax-2*t)*tan(alpha))/3) - z)**2 

    Ix_lower_triangle_inner = (1/36) * (deltax-2*t)*(((deltax-2*t)*tan(beta))**3)+(((deltax-2*t)*(deltax-2*t)*tan(beta))/2)*(z-(t+(2/3)*(deltax-2*t)*tan(beta)))**2 

    Ix_total = Ix_rectangle_outer + Ix_upper_triangle_outer + Ix_lower_triangle_outer - Ix_upper_triangle_inner - Ix_lower_triangle_inner - Ix_rectangle_inner

    return (Ix_total)




   
def Izcalculator(deltax,b,alpha,beta,t,x,z):

    Iz_rectangle_outer = (1/12) * (deltax**3) * b + deltax * b * ((l/2)-x)**2 

    Iz_upper_triangle_outer = (1/36) * (deltax**3) * deltax * tan(alpha) + ((deltax*deltax*tan(alpha))/2)*(x- (l/3))**2 

    Iz_lower_triangle_outer = (1/36) * (deltax**3) * deltax * tan(beta) + ((deltax*deltax*tan(beta))/2)*(x- (l/3))**2 

    Iz_rectangle_inner = (1/12) * ((deltax - 2 *t)**3)*(b-2*t) + (deltax-2*t) * (b - 2*t)*((t+(1/2)*(deltax-2*t))-x)**2 

    Iz_upper_triangle_inner = (1/36) * ((deltax-2*t)**3)*(deltax-2*t)*tan(alpha)+((((deltax-2*t)**2)*tan(alpha))/2)*(x-(t+((l-2*t)/3)))**2 

    Iz_lower_triangle_inner = (1/36) * ((deltax-2*t)**3)*(deltax-2*t)*tan(beta)+((((deltax-2*t)**2)*tan(beta))/2)*(x-(t+((deltax-2*t)/3)))**2 

    Iz_total = Iz_rectangle_outer + Iz_upper_triangle_outer + Iz_lower_triangle_outer - Iz_upper_triangle_inner - Iz_lower_triangle_inner - Iz_rectangle_inner


    return(Iz_total)




#outputs: moment of inertia of shape for x and z direction
