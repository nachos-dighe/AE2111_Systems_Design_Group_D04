from math import tan
import math

l = 2
b = 1
theta = 0.7
beta = 0.6
t = 0.1
x = 2
y = 1




#Angles in radians!!!

#inputs needed: theta2 (defined as theta here), theta3 (beta here), delta x s (l here), b2 (b here), t (thickness defined for first time), position of cg (x and y here)

def Ixcalculator(l,b,theta,beta,t,x,y):
    
    Ix_rectangle_outer = (1/12)* l * (b**3) + l * b * (y - (l*tan(beta)+(b/2)))**2 
    
    Ix_upper_triangle_outer = (1/36) * l * ((l* tan(theta))**3) + ((l*l*tan(theta))/2)*(l*tan(beta)+b+(1/3)*l*tan(theta)-y)**2

    Ix_lower_triangle_outer = (1/36) * l * ((l* tan(beta))**3) + ((l*l*tan(beta))/2)*(y-((2/3)*l*tan(beta)))**2 

    Ix_rectangle_inner = (1/12)*(l-2*t)*((b-2*t)**3)+(l-2*t)*(b-2*t)*(t+y-(t+(l-2*t)*tan(beta)+((b-2*t)/2)))**2 

    Ix_upper_triangle_inner = (1/36) * (l-2*t)*(((l-2*t)*tan(theta))**3)+(((l-2*t)*(l-2*t)*tan(theta))/2)*(t+(l-2*t)*tan(beta)+b-2*t+((l-2*t)*tan(theta))/3 - x - t)**2 

    Ix_lower_triangle_inner = (1/36) * (l-2*t)*(((l-2*t)*tan(beta))**3)+(((l-2*t)*(l-2*t)*tan(beta))/2)*(t+y-(t+(2/3)*(l-2*t)*tan(beta)))**2

    Ix_total = Ix_rectangle_outer + Ix_upper_triangle_outer + Ix_lower_triangle_outer - Ix_upper_triangle_inner - Ix_lower_triangle_inner - Ix_rectangle_inner

    return (Ix_total)



#print(Ixcalculator(l,b,theta,beta,t,x,y))

   
def Iycalculator(l,b,theta,beta,t,x,y):

    Iy_rectangle_outer = (1/12) * (l**3) * b + l * b * ((l/2)-x)**2

    Iy_upper_triangle_outer = (1/36) * (l**3) * l * tan(theta) + ((l*l*tan(theta))/2)*(x- (l/3))**2

    Iy_lower_triangle_outer = (1/36) * (l**3) * l * tan(beta) + ((l*l*tan(beta))/2)*(x- (l/3))**2

    Iy_rectangle_inner = (1/12) * ((l - 2 *t)**3)*(b-2*t) + (l-2*t) * (b - 2*t)*(t+(1/2)*(l-2*t)-(x+t))**2

    Iy_upper_triangle_inner = (1/36) * ((l-2*t)**3)*(l-2*t)*tan(theta)+((((l-2*t)**2)*tan(theta))/2)*(x+t-(t+((l-2*t)/3)))**2

    Iy_lower_triangle_inner = (1/36) * ((l-2*t)**3)*(l-2*t)*tan(beta)+((((l-2*t)**2)*tan(beta))/2)*(x+t-(t+((l-2*t)/3)))**2

    Iy_total = Iy_rectangle_outer + Iy_upper_triangle_outer + Iy_lower_triangle_outer - Iy_upper_triangle_inner - Iy_lower_triangle_inner - Iy_rectangle_inner

    return(Iy_total)

#print(Iycalculator(l,b,theta,beta,t,x,y))



#outputs: moment of inertia of shape for x and y direction
