import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


# Geometric
RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span
dT = 5

# Explanation of variables
#                    b
#             |-----------\
#             |(alpha)     \------|
# front spar  |a                 c| rear spar
#             |(beta)      /------|
#             |-----------/
#                    

# RCr = rood chord length
# TCr = tip chord length
# FSparL = List of front spar lengths (a)
# RSparL = List of rear spar length (b)
# Lengthbox = List of total length of wingbox
# Cr = local chord length
# y = The y  position of all the length from root to tip



# Calculations
def WingboxDimensions(RCr, TCr, Span, dT):
    y = 0
    FSparL = []
    RSparL =  []
    LengthBox =  []
    Cr = []
    while y <= Span/2 :

        Cr = RCr - (RCr-TCr)/Span * y

        FSparL.append(round(0.08562876 * Cr,3)) # a The value given was generated in Catia
        RSparL.append(round(0.05423628 * Cr,3)) # b The value given was generated in Catia
        LengthBox.append(round((0.75-0.2) * Cr,3)) # b

        Theta2 = (2.54121433)*(3.14159265359/180) # rad
        Theta3 = (0.72736298)*(3.14159265359/180)  # rad

        y = y + dT

        b2 = RSparL
        DeltaX = LengthBox

    return  Theta2, Theta3, b2, DeltaX, Cr, y 

## Test code
##Theta2, Theta3, b2, DeltaX, Cr, y = WingboxDimensions(RCr, TCr, Span, 0.1)
##print(Theta2*3.1415, Theta3*3.1415)















