import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

aero_data_AOA_0 = np.genfromtxt('MainWing_a=0.00_v=10.00ms.txt', dtype = float, skip_header=2)
aero_data_AOA_10 = np.genfromtxt('MainWing_a=10.00_v=10.00ms.txt', dtype = float, skip_header=2)

#testing works
print(aero_data_AOA_0)
Cdlst = aero_data_AOA_0[:, 5]
print(Cdlst)


def aero_coefficient(aero_data_AOA):
    ylst = aero_data_AOA[:,0]
    Cllst = aero_data_AOA[:,3]
    Cdlst = aero_data_AOA[:, 5]
    print(Cdlst)
    Cmlst = aero_data_AOA[:, 7] #pitching moment about c/4 point
    return(ylst,Cllst, Cdlst, Cmlst)

ylst_0,Cllst_0, Cdlst_0, Cmlst_0 = aero_coefficient(aero_data_AOA_0)
ylst_10,Cllst_10, Cdlst_10, Cmlst_10 = aero_coefficient(aero_data_AOA_10)
