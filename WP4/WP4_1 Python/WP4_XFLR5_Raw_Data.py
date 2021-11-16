import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
exec(open("Aircraft.py").read())


#print(Wingspan) #testing works, but find a better implementation method

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
    xlst_init = aero_data_AOA[:,1]
    ylst_init = aero_data_AOA[:,0]
    Cllst_init = aero_data_AOA[:,3]
    Cdlst_init = aero_data_AOA[:, 5]
    #print(Cdlst) #testing
    Cmlst_init = aero_data_AOA[:, 7] #pitching moment about c/4 point
    return(xlst_init,ylst_init,Cllst_init, Cdlst_init, Cmlst_init)

#interpolation
def interpolation(xlst_init,ylst_init,Cllst_init, Cdlst_init, Cmlst_init):
    ylst = np.linspace(min(ylst_init), max(ylst_init), num=100, endpoint=True)
    
    Cl_interp = sp.interpolate.interp1d(ylst_init,Cllst_init, kind = "cubic", fill_value="extrapolate")
    Cd_interp = sp.interpolate.interp1d(ylst_init,Cdlst_init, kind = "cubic", fill_value="extrapolate")
    Cm_interp = sp.interpolate.interp1d(ylst_init,Cmlst_init, kind = "cubic", fill_value="extrapolate")
    x_interp = sp.interpolate.interp1d(ylst_init,xlst_init, kind = "linear", fill_value ="extrapolate")
    
    #Making the size of interpolation lists the same
    Cllst = Cl_interp(ylst)
    Cdlst = Cd_interp(ylst)
    Cmlst = Cm_interp(ylst)
    xlst = x_interp(ylst)   
    return(xlst,ylst,Cllst, Cdlst, Cmlst)

#aerodynamics loads (dimensional)
def aero_loads(xlst, ylst,Cllst, Cdlst, Cmlst):
    v_cruise = 243.13
    rho_cruise = 0.37956
    q_cruise = 0.5*rho_cruise*v_cruise**2
    N_z_positive = 2.5  #change later
    N_z_negative = 1.5  #change later
   
    #HALF-wing weight
<<<<<<< HEAD
    W_wing =  40,209.08
=======
    W_wing =  40209.08
>>>>>>> 9ffd309e4bf6484aebb75e502dca7dbd7e4ab40b
    W_half_wing = W_wing/2
    taper = 0.4
    b = 24.63
    
    W_root = 2*W_wing/((1+taper)*b)
    Wlst = W_root*(1+2/b*(taper-1)*ylst)
<<<<<<< HEAD
    
=======
>>>>>>> 9ffd309e4bf6484aebb75e502dca7dbd7e4ab40b
    
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
    
    #distributed load along span (coordinate system: downward)
    Fzreslst = Wlst-Llst 
<<<<<<< HEAD
    
    return(Llst,Dlst,Mlst, Fzreslst, Ltot, Dtot, Mtot)

=======
    return(Llst,Dlst,Mlst, Fzreslst, Ltot, Dtot, Mtot)
>>>>>>> 9ffd309e4bf6484aebb75e502dca7dbd7e4ab40b

def aero_plots(ylst,Llst,Dlst,Mlst, Fzreslst, Ltot, Dtot, Mtot):
    
    print('Total lift is', Ltot, ' ' ,'Total drag is', Dtot, ' ' , 'Total moment is', Mtot, ' ' ,sep ='\n')
    
    fig, axs = plt.subplots(3, figsize=(8,8))
    axs[0].plot(ylst,Llst)
    axs[0].set_title('Lift')
    axs[1].plot(ylst,Dlst)
    axs[1].set_title('Drag')
    axs[2].plot(ylst, Mlst)
    axs[2].set_title('Moment')
    fig.suptitle('Aerodynamic loading', fontsize=16)
    fig.tight_layout()
    plt.show()
    return()

#lists for aerodynamic coefficients 
xlst_0,ylst_0,Cllst_0, Cdlst_0, Cmlst_0 = aero_coefficient(aero_data_AOA_0)
xlst_10,ylst_10,Cllst_10, Cdlst_10, Cmlst_10 = aero_coefficient(aero_data_AOA_10)

<<<<<<< HEAD
#lists for aerodynamic loads
Llst_0,Dlst_0,Mlst_0, Fzreslst_0,Ltot_0, Dtot_0, Mtot_0 = aero_loads(xlst_0, ylst_0,Cllst_0, Cdlst_0, Cmlst_0)
Llst_10,Dlst_10,Mlst_10, Fzreslst_10, Ltot_10, Dtot_10, Mtot_10 = aero_loads(xlst_10, ylst_10,Cllst_10, Cdlst_10, Cmlst_10)
=======
#interpolation of above aero coefficients
xlst_0,ylst_0,Cllst_0, Cdlst_0, Cmlst_0 = interpolation(xlst_0,ylst_0,Cllst_0, Cdlst_0, Cmlst_0)
xlst_10,ylst_10,Cllst_10, Cdlst_10, Cmlst_10 = interpolation(xlst_10,ylst_10,Cllst_10, Cdlst_10, Cmlst_10)
>>>>>>> 9ffd309e4bf6484aebb75e502dca7dbd7e4ab40b


#design lift coefficient distribution
Cltot_des = 0.372976647
Cltot_0 = 0.264851185
Cltot_10 = 1.324255925

#obtain design angle of attack
Cllst_des =  Cllst_0 + (Cltot_des-Cltot_0)/(Cltot_10-Cltot_0)*(Cllst_10-Cllst_0)
alpha_des = np.arcsin((np.sum(Cllst_des)-np.sum(Cllst_0))/(np.sum(Cllst_10)-np.sum(Cllst_0))*np.sin(np.deg2rad(10)))
Cdlst_des = alpha_des/(10-0)*(Cdlst_10-Cdlst_0)
Cmlst_des = alpha_des/(10-0)*(Cmlst_10-Cmlst_0)
#print("Design angle of attack is", np.rad2deg(alpha_des)) #testing works

''' #do not use 
alpha_des = (10-0)*(np.sum(Cllst_des)-np.sum(Cllst_0))/(np.sum(Cllst_0)-np.sum(Cllst_10))
print(alpha_des) #testing
'''

#testing 
#print(Ltot_des*2, Dtot_des*2, Mtot_des*2)

#lists for aerodynamic loads
Llst_0,Dlst_0,Mlst_0, Fzreslst_0,Ltot_0, Dtot_0, Mtot_0 = aero_loads(xlst_0, ylst_0,Cllst_0, Cdlst_0, Cmlst_0)
Llst_10,Dlst_10,Mlst_10, Fzreslst_10, Ltot_10, Dtot_10, Mtot_10 = aero_loads(xlst_10, ylst_10,Cllst_10, Cdlst_10, Cmlst_10)
Llst_des,Dlst_des,Mlst_des, Fzreslst_des,Ltot_des, Dtot_des, Mtot_des = aero_loads(xlst_0, ylst_0,Cllst_des, Cdlst_des, Cmlst_des)

#plot for design condition
aero_plots(ylst_0, Llst_des, Dlst_des, Mlst_des, Fzreslst_des, Ltot_des, Dtot_des, Mtot_des)






<<<<<<< HEAD
#testing 
#print(Ltot_des*2, Dtot_des*2, Mtot_des*2)


ynew = np.linspace(min(ylst_0), max(ylst_0), num=100, endpoint=True)

#interpolation
Cl_interp0 = sp.interpolate.interp1d(ylst_0,Cllst_0, kind = "cubic", fill_value="extrapolate")
Cd_interp0 = sp.interpolate.interp1d(ylst_0,Cdlst_0, kind = "cubic", fill_value="extrapolate")
Cm_interp0 = sp.interpolate.interp1d(ylst_0,Cmlst_0, kind = "cubic", fill_value="extrapolate")
x_interp0 = sp.interpolate.interp1d(ylst_0,xlst_0, kind = "linear", fill_value ="extrapolate")

v_cruise = 243.13
rho_cruise = 0.37956
q_cruise = 0.5*rho_cruise*v_cruise**2
#Making the size of interpolation lists the same (for angle 0)
Cl_new0 = Cl_interp0(ynew)
Cd_new0 = Cd_interp0(ynew)
Cm_new0 = Cm_interp0(ynew)
x_new0 = x_interp0(ynew)
Llst = Cl_new0*q_cruise*x_new0
Dlst = Cd_new0*q_cruise*x_new0
Mlst = Cm_new0*x_new0**2*q_cruise

fig, axs = plt.subplots(3, figsize=(8,8))
axs[0].plot(ynew,Llst)
axs[0].set_title('Lift')
axs[1].plot(ynew,Dlst)
axs[1].set_title('Drag')
axs[2].plot(ynew, Mlst)
axs[2].set_title('Moment')
plt.show()
'''
ax[2,0].plot(ynew,Mlst)
ax[2,0].set_title('Moment')
plt.show()'''

=======





























'''
ax[2,0].plot(ynew,Mlst)
ax[2,0].set_title('Moment')
plt.show()'''

>>>>>>> 9ffd309e4bf6484aebb75e502dca7dbd7e4ab40b
'''
Llst = []
Dlst = []

for i in ylst_0:
    Llst.append(Cl_interp0(i)*x_interp0(i)*q_cruise)
    #Dlst.append(Cd_interp0(i)*x_interp0(i)*q_cruise)
plt.plot(ylst_0,Llst)    #blue line
plt.plot(ylst_0,Dlst)   #orange line
#plt.show()
#Mlst = Cm_interp0(i)*xlst**2*q_cruise
'''


#testing
#M_cr = 0.82
#beta = (1-M_cr**2)**-0.5

#fig, axs = plt.subplots(2,2)
#fig.suptitle('Lift distribution along span')
#axs[0,0].plot(ylst_0, Llst_0)
#axs[0,0].set_title('0 deg AOA')
#axs[0,1].plot(ylst_10, Llst_10)
#axs[0,1].set_title('10 deg AOA')
#axs[1,0].plot(ylst_10, Llst_des)
#axs[1,0].set_title('cruise deg AOA: \n comp correction')
#axs[1,1].plot(ylst_10, Llst_des/beta)
#axs[1,1].set_title('cruise deg AOA: \n w/o comp correction')
#fig.tight_layout()
#plt.show()


