from math import tan, cos, pi

def J_calculation(Theta2, Theta3, b2, DeltaX, t):
    
    #intermediate outputs
    circumference = 2*b2 + DeltaX * ((1/cos(Theta2)) + tan(Theta2) + (1/cos(Theta3)) + tan(Theta3))
    A = (0.5 * DeltaX * tan(Theta2)) + (0.5 * DeltaX * tan(Theta3)) + b2*DeltaX
    line_integral = circumference / t
    
    #final
    J = (4*A*A)/line_integral
    return J
