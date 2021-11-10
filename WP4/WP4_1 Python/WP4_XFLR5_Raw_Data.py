import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

aero_data_AOA_0 = np.genfromtxt('MainWing_a=0.00_v=10.00ms.txt', dtype = float, skip_header=2)
aero_data_AOA_10 = np.genfromtxt('MainWing_a=10.00_v=10.00ms.txt', dtype = float, skip_header=2)

'''
#testing works
print(aero_data_AOA_0)
Cdlst = aero_data_AOA_0[:, 5]
print(Cdlst)
'''

def aero_coefficient(aero_data_AOA):
    ylst = aero_data_AOA[:,0]
    Cllst = aero_data_AOA[:,3]
    Cdlst = aero_data_AOA[:, 5]
    Cmlst = aero_data_AOA[:, 7] #pitching moment about c/4 point
    return(ylst,Cllst, Cdlst, Cmlst)

ylst_0,Cllst_0, Cdlst_0, Cmlst_0 = aero_coefficient(aero_data_AOA_0)
ylst_10,Cllst_10, Cdlst_10, Cmlst_10 = aero_coefficient(aero_data_AOA_10)


#aerodynamics loads (dimensional)
def aero_loads(xlst, ylst,Cllst, Cdlst, Cmlst):
    v_cruise = 243.13
    rho_cruise = 0.37956
    q_cruise = 0.5*rho_cruise*v_cruise**2
    Llst = Cllst*xlst*q_cruise
    Dlst = CDlst*xlst*q_cruise
    Mlst = Cmlst*xlst**2*q_cruise #pitching moment about c/4 point

    #total aerodynamic loads
    Ltot = np.sum(Llst)
    Dtot = np.sum(Dlst)
    Mtot = np.sum(Mlst)
    return(Llst,Dlst,Mlst, Ltot, Dtot, Mtot)

    Llst_0,Dlst_0,Mlst_0, Ltot_0, Dtot_0, Mtot_0 = aero_loads(xlst_0, ylst_0,Cllst_0, Cdlst_0, Cmlst_0)
    Llst_10,Dlst_10,Mlst_10, Ltot_10, Dtot_10, Mtot_10 = aero_loads(xlst_10, ylst_10,Cllst_10, Cdlst_10, Cmlst_10)





