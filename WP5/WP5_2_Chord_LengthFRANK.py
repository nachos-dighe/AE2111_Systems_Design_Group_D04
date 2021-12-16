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
# b = List of rear spar length (b)
# DeltaX = List of total length of wingbox
# Cr = local chord length
# y = The y  position of all the length from root to tip



# Calculations
def WingboxDimensions(RCr, TCr, Span, ylst):
    FSparL = []
    b =  []
    DeltaX =  []
    Cr = []
    i = 0
    while i <= 999 :
        ylst[i] = float(ylst[i])
        Cr_RAW = RCr - (RCr-TCr)/(Span/2)* ylst[i]
        Cr.append(Cr_RAW)
        FSparL.append(round(0.08562876 * Cr_RAW,3)) # a The value given was generated in Catia
        b.append(round(0.05423628 * Cr_RAW,3)) # b The value given was generated in Catia
        DeltaX.append(round((0.75-0.2) * Cr_RAW,3)) # b

        alpha = (2.54121433)*(3.14159265359/180) # rad
        beta = (0.72736298)*(3.14159265359/180)  # rad

        i = i + 1

    return  alpha, beta, b, DeltaX, Cr 

## Test code
##alpha, beta, b2, DeltaX, Cr, y = WingboxDimensions(RCr, TCr, Span, 1)
##print(alpha, beta, b2[0], DeltaX[0], Cr)















