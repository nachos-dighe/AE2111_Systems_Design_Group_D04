from math import tan, cos, pi

def J_calculation(Theta2, Theta3, b2, DeltaX, t):
    
    #intermediate outputs
    circumference = 2*b2 + DeltaX * ((1/cos(Theta2)) + (1/tan(Theta2)) + (1/cos(Theta3)) + (1/tan(Theta3)))
    A = t * circumference
    line_integral = circumference / t
    
    #final
    J = (4*A*A)/line_integral
    return J

Theta2 = 1
Theta3 = 1
b2 = 1
DeltaX = 1
t = 0.01
J = J_calculation(Theta2, Theta3, b2, DeltaX, t)
print(J)
