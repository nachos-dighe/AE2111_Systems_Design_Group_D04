from math import tan
import math


#Angles in radians!!!

def Ixcalculator():
    Ix_rectangle_outer = (1/12)* l * (b**3) + l * b * (y - (l*tan(beta)+(b/2)))**2
    
    Ix_upper_triangle_outer = (1/36) * l * ((l* tan(theta))**3) + ((l*l*tan(theta))/2)*(l*tan(beta)+b+(1/3)*l*tan(theta)-y)**2

    Ix_lower_triangle_outer = (1/36) * l * ((l* tan(beta))**3) + ((l*l*tan(beta))/2)*(y-((2/3)*l*tan(beta)))**2 

    Ix_rectangle_inner = (1/12)*(l-2t)*((b-2*t)**3)+(l-2*t)*(b-2*t)*(t+y-(t+(l-2*t)*tan(beta)+((b-2*t)/2)))**2

    Ix_upper_triangle_inner = (1/36) * (l-2*t)*(((l-2*t)*tan(theta))**3)+(((l-2*t)*(l-2*t)*tan(theta))/2)*(t+(l-2*t)*tan(beta)+b-2*t+((l-2*t)*tan(theta))/3 - x - t)**2

    Ix_lower_triangle_inner = (1/36) * (l-2*t)*(((l-2*t)*tan(beta))**3)+(((l-2*t)*(l-2*t)*tan(beta))/2)*(t+y-(t+(2/3)*(l-2*t)*tan(beta)))**2

    Ix_total = Ix_rectangle_outer + Ix_upper_triangle_outer + Ix_lower_triangle_outer - Ix_upper_triangle_inner - Ix_lower_triangle_inner - Ix_rectangle_inner


    return(Ix_total)
    
def Iycalculator():

    Iy_rectangle_outer = (1/12) * (l**3) * b + l * b * ((l/2)-x)**2

    Iy_upper_triangle_outer = (1/36) * (l**3) * l * tan(theta) + ((l*l*tan(theta))/2)*(x- (l/3))**2

    Iy_lower_triangle_outer = (1/36) * (l**3) * l * tan(beta) + ((l*l*tan(beta))/2)*(x- (l/3))**2

    Iy_rectangle_inner =

    Iy_upper_triangle_inner =

    Iy_lower_triangle_inner = 
        


print(Ix_total)



