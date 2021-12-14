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
    l = 0
    dT = ( Span / 2 ) / dy
    y_lst = []

    # Reading the y positions from the file 
    with open("ylst.dat", "r") as file : # Reads the y position file 
        y_lstRAW = file.readlines()

    for line in y_lstRAW :
        y = line.replace(",", "")
        y = float(y)
        y_lst.append(y)


    
    alpha, beta, b2, DeltaX, Cr = Lengths.WingboxDimensions(RCr, TCr, Span, y_lst)
    while l <= 999 :
        
        l = l +1
        j = i - 1
        c = DeltaX[j] * tan(alpha)
        d = DeltaX[j] * tan(beta)

        m1 = ((DeltaX[j]) / (cos(alpha)))
        m2 = b2[j] + c + d
        m3 = b2[j]
        m4 = ((DeltaX[j]) / (cos(beta)))
        
        x1 = 0.5 * DeltaX[j]
        x2 = 0
        x3 = DeltaX[j]
        x4 = 0.5 * DeltaX[j]

        z1 = b2[j] + d + 0.5 * c
        z2 = d + 0.5 * b2[j]
        z3 = d + 0.5 * b2[j]
        z4 = 0.5 * d

        CG_x = (m1*x1 + m2*x2 + m3*x3 + m4*x4)/(m1 + m2 + m3 + m4)
        CG_z = (m1*z1 + m2*z2 + m3*z3 + m4*z4)/(m1 + m2 + m3 + m4)

        CG_xList.append(CG_x)
        CG_zList.append(CG_z)
        i = i + 1
        #FracX = CG_x/CrList[j] # This are the relavtive positions of the CG comapred to the chord length
        #FracZ = CG_z/CrList[j] # This are the relavtive positions of the CG comapred to the chord length
    return CG_xList, CG_zList, Cr

CG_xList, CG_zList, Cr = cg_calculation(999)












    
