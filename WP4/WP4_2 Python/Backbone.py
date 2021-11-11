# Geometric
RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 0.1
i = 0

CG_XList = []
CG_ZList = []


import Chord_Length as Lengths
import CG_wingbox as CG

Theta2, Theta3, b2, DeltaX, Cr, y = Lengths.WingboxDimensions(RCr, TCr, Span, dT)

print(y)


while (dT * i)<= Span/2 :
    CG_x, CG_z = CG.cg_calculation(Theta2, Theta3, b2[i], DeltaX[i])
    CG_XList.append(CG_x)
    CG_ZList.append(CG_z)

    i = i +1
print(CG_XList)
print(CG_ZList)
    


















