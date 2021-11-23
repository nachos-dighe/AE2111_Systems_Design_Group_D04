from math import tan, pi 

Theta2 = (2.54) * 0.0174532925
Theta3 = (0.73) * 0.0174532925
b2     = 5.42
DeltaX = 55

# Explanation of variables
#
# Lengths
#                 Delta x
#             |-----------\      c
#             |(Theta2)    \------|
# front spar  |a                 b| rear spar
#             |(Theta3)    /------|
#             |-----------/      d
#

# Naming of each part
#
#                    m1
#             |-----------\
#             |            \------|
#           m2|                   | m3
#             |            /------|
#             |-----------/
#                    m4
#         


def cg_calculation(Theta2, Theta3, b2, DeltaX):
    c = DeltaX * tan(Theta2)
    d = DeltaX * tan(Theta3)

    m1 = ((DeltaX) / (cos(Theta2)))
    m2 = b + c + d
    m3 = b
    m4 = ((DeltaX) / (cos(Theta3)))
    
    x1 = 0.5 * DeltaX
    x2 = 0
    x3 = DeltaX
    x4 = 0.5 * DeltaX

    z1 = b + d + 0.5 * c
    z2 = d + 0.5 * b
    z3 = d + 0.5 * b
    z4 = 0.5 * d

    CG_x = (m1*x1 + m2*x2 + m3*x3 + m4*x4)/(m1 + m2 + m3 + m4)
    CG_y = (m1*z1 + m2*z2 + m3*z3 + m4*z4)/(m1 + m2 + m3 + m4)

    return CG_x, CG_y














    
