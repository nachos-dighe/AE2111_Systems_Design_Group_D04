from math import tan, pi, cos, sin

alpha = (2.54) * 0.0174532925
beta = (0.73) * 0.0174532925
b2     = 5.42
DeltaX = 55
i = 0


CG_xList = []
CG_zList = []
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
import Chord_Length as Lengths 

def cg_calculation(dy):
    RCr = 4.4 # [m] Root chord
    TCr = 1.76 # [m] Tip chord
    Span = 24.64 # [m] Span
    i = 0
    dT = 1/dy
    alpha, beta, b2, DeltaX, Cr, y = Lengths.WingboxDimensions(RCr, TCr, Span, dT)
    
    while (dT * i ) <= Span/2 :
        c = DeltaX[i] * tan(alpha)
        d = DeltaX[i] * tan(beta)

        m1 = ((DeltaX[i]) / (cos(alpha)))
        m2 = b2[i] + c + d
        m3 = b2[i]
        m4 = ((DeltaX[i]) / (cos(beta)))
        
        x1 = 0.5 * DeltaX[i]
        x2 = 0
        x3 = DeltaX[i]
        x4 = 0.5 * DeltaX[i]

        z1 = b2[i] + d + 0.5 * c
        z2 = d + 0.5 * b2[i]
        z3 = d + 0.5 * b2[i]
        z4 = 0.5 * d

        CG_x = (m1*x1 + m2*x2 + m3*x3 + m4*x4)/(m1 + m2 + m3 + m4)
        CG_z = (m1*z1 + m2*z2 + m3*z3 + m4*z4)/(m1 + m2 + m3 + m4)

        CG_xList.append(CG_x)
        CG_zList.append(CG_z)
        i = i + 1

    return CG_xList, CG_zList


CG_xList, CG_zList = cg_calculation(1000)












    
