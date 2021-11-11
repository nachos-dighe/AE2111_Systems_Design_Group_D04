import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate

#import XFLR5 data for AOA 0 and 10 deg
aero_data_AOA_0 = np.genfromtxt('MainWing_a=0.00_v=10.00ms.txt', dtype = float, skip_header=2)
aero_data_AOA_10 = np.genfromtxt('MainWing_a=10.00_v=10.00ms.txt', dtype = float, skip_header=2)

#testing works
'''
print(aero_data_AOA_0)
Cdlst = aero_data_AOA_0[:, 5]
print(Cdlst)
'''

#aerodynamics coefficients (non-dimensional)
def aero_coefficient(aero_data_AOA):
    xlst = aero_data_AOA[:,1]
    ylst = aero_data_AOA[:,0]
    Cllst = aero_data_AOA[:,3]
    Cdlst = aero_data_AOA[:, 5]
    #print(Cdlst) #testing
    Cmlst = aero_data_AOA[:, 7] #pitching moment about c/4 point
    return(xlst,ylst,Cllst, Cdlst, Cmlst)

#aerodynamics loads (dimensional)
def aero_loads(xlst, ylst,Cllst, Cdlst, Cmlst):
    v_cruise = 243.13
    rho_cruise = 0.37956
    q_cruise = 0.5*rho_cruise*v_cruise**2
    
    #Prandtl-Glauert compressibility correction
    M_cr = 0.82
    beta = (1-M_cr**2)**-0.5
    Llst = Cllst*xlst*q_cruise*beta
    Dlst = Cdlst*xlst*q_cruise*beta
    Mlst = Cmlst*xlst**2*q_cruise*beta #pitching moment about c/4 point

    #total aerodynamic loads
    Ltot = np.sum(Llst)
    Dtot = np.sum(Dlst)
    Mtot = np.sum(Mlst)
    return(Llst,Dlst,Mlst, Ltot, Dtot, Mtot)


#lists for aerodynamic coefficients
xlst_0,ylst_0,Cllst_0, Cdlst_0, Cmlst_0 = aero_coefficient(aero_data_AOA_0)
xlst_10,ylst_10,Cllst_10, Cdlst_10, Cmlst_10 = aero_coefficient(aero_data_AOA_10)

#lists for aerodynamic loads
Llst_0,Dlst_0,Mlst_0, Ltot_0, Dtot_0, Mtot_0 = aero_loads(xlst_0, ylst_0,Cllst_0, Cdlst_0, Cmlst_0)
Llst_10,Dlst_10,Mlst_10, Ltot_10, Dtot_10, Mtot_10 = aero_loads(xlst_10, ylst_10,Cllst_10, Cdlst_10, Cmlst_10)


#design lift coefficient distribution
Cltot_des = 0.372976647
Cltot_0 = 0.264851185
Cltot_10 = 1.324255925
Cllst_des =  Cllst_0 + (Cltot_des-Cltot_0)/(Cltot_10-Cltot_0)*(Cllst_10-Cllst_0)

#obtain design angle of attack

alpha_des = np.arcsin((np.sum(Cllst_des)-np.sum(Cllst_0))/(np.sum(Cllst_10)-np.sum(Cllst_0))*np.sin(np.deg2rad(10)))
print("Design angle of attack is", np.rad2deg(alpha_des)) #testing works

''' #do not use 
alpha_des = (10-0)*(np.sum(Cllst_des)-np.sum(Cllst_0))/(np.sum(Cllst_0)-np.sum(Cllst_10))
print(alpha_des) #testing
'''

Cdlst_des = alpha_des/(10-0)*(Cdlst_10-Cdlst_0)
Cmlst_des = alpha_des/(10-0)*(Cmlst_10-Cmlst_0)


Llst_des,Dlst_des,Mlst_des, Ltot_des, Dtot_des, Mtot_des = aero_loads(xlst_0, ylst_0,Cllst_des, Cdlst_des, Cmlst_des)

#testing 
print(Ltot_des*2, Dtot_des*2, Mtot_des*2)

#interpolation
Cl_interp0 = sp.interpolate.interp1d(ylst_0,Cllst_0, kind = "cubic", fill_value="extrapolate")
Cd_interp0 = sp.interpolate.interp1d(ylst_0,Cdlst_0, kind = "cubic", fill_value="extrapolate")
Cm_interp0 = sp.interpolate.interp1d(ylst_0,Cmlst_0, kind = "cubic", fill_value="extrapolate")
x_interp0 = sp.interpolate.interp1d(ylst_0,xlst_0, kind = "linear", fill_value ="extrapolate")

v_cruise = 243.13
rho_cruise = 0.37956
q_cruise = 0.5*rho_cruise*v_cruise**2


#FOR ZERO ALPHA
Llst = []
for i in ylst_0:
    Llst.append(Cl_interp0(i)*x_interp0(i)*q_cruise)
Dlst = []
for j in ylst_0:
    Dlst.append(Cd_interp0(j)*x_interp0(j)*q_cruise)
plt.plot(ylst_0,Llst)    #blue line
plt.plot(ylst_0,Dlst)   #orange line
print(len(Llst), len(Dlst))
plt.show()
#Mlst = Cm_interp0(i)*xlst**2*q_cruise



#testing
M_cr = 0.82
beta = (1-M_cr**2)**-0.5

fig, axs = plt.subplots(2,2)
fig.suptitle('Lift distribution along span')
axs[0,0].plot(ylst_0, Llst_0)
axs[0,0].set_title('0 deg AOA')
axs[0,1].plot(ylst_10, Llst_10)
axs[0,1].set_title('10 deg AOA')
axs[1,0].plot(ylst_10, Llst_des)
axs[1,0].set_title('cruise deg AOA: \n comp correction')
axs[1,1].plot(ylst_10, Llst_des/beta)
axs[1,1].set_title('cruise deg AOA: \n w/o comp correction')
fig.tight_layout()
plt.show()


