from math import * 

alpha = (2.54) * 0.0174532925
beta = (0.73) * 0.0174532925
b     = 5.42
DeltaX = 55

# Explanation of variables
#
# Lengths
#                 Delta x
#             |-----------\      c
#             |(alpha)    \------|
# front spar  |a                 b| rear spar
#             |(beta)    /------|
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


def cg_calculation(alpha, beta, b, DeltaX):
    c = DeltaX * tan(alpha)
    d = DeltaX * tan(beta)

    m1 = ((DeltaX) / (cos(alpha)))
    m2 = b + c + d
    m3 = b
    m4 = ((DeltaX) / (cos(beta)))
    
    x1 = 0.5 * DeltaX
    x2 = 0
    x3 = DeltaX
    x4 = 0.5 * DeltaX

    z1 = b + d + 0.5 * c
    z2 = d + 0.5 * b
    z3 = d + 0.5 * b
    z4 = 0.5 * d

    CG_x =   (m1*x1 + m2*x2 + m3*x3 + m4*x4)/(m1 + m2 + m3 + m4)
    CG_z = -((m1*z1 + m2*z2 + m3*z3 + m4*z4)/(m1 + m2 + m3 + m4))

    return CG_x, CG_z














    
