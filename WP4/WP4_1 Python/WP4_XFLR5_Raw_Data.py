import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.integrate import simps, cumtrapz
#exec(open("Aircraft.py").read())
#print(Wingspan) #testing works, but find a better implementation method. Ignore use of parametric python file for now.

#constants
g = 9.80665
#wing
b = 24.63
taper = 0.4
S_wing = 76.29

#sweep angle calculation
Sw_ca = np.arctan( np.tan (25 / 180 * np.pi ) -  ( 0.468 * ( 2 * 4.41 ) / b ) * ( 1 - 0.4 ) )

#aircraft weight
W_pl = 9800*g
W_oe = 20175*g
W_mto = 33139*g
W_f = W_mto - W_oe-W_pl
W_ac_lst = [W_oe, W_mto, W_oe+W_pl]


###----HARD-CODE------ ### (START)
W_ac = W_ac_lst[1] #(0,1,2) #aircraft weight #FIXED
is_fuel = True #(True, False) #fuel in wing boolean #FIXED
v_cruise = 120 #velocity #this may change depending on critical loading case #FIXED: LOWEST speed that gives 2.5 (190m/s);LOWEST speed that gives -1 (120m/s)
rho_cruise =0.37956  #density #this may change depending on critical loading case (1.225,0.37956)
###----HARD-CODE------ ### (END)


#dynamic pressure
q_cruise = 0.5 * rho_cruise * v_cruise ** 2 
#q_cruise = 0.5 * rho_cruise * v_cruise ** 2 * np.cos( Sw_ca )  #sweep does not affect dynamic pressure

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
    Cdlst_init = aero_data_AOA[:, 5] #induced drag
    Cmlst_init = aero_data_AOA[:, 7] #pitching moment about c/4 point
    
    #airfoil characteristics 
    Cm_airfoil = 8.42E-02
    Cd_airfoil = 0.01 #form drag for low AOA
    
    Cdlst_init = Cdlst_init + Cd_airfoil
    #print(Cdlst_init) #testing

    return(xlst_init,ylst_init,Cllst_init, Cdlst_init, Cmlst_init)

#interpolation
def interpolation(xlst_init,ylst_init,Cllst_init, Cdlst_init, Cmlst_init):
    ylst = np.linspace(min(ylst_init), max(ylst_init), num=1000, endpoint=True)
    
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
    
    #based on ref data, approx. 30% of fuel weight is stored in wing (from root to 0.55/2 spar: consider inner tank only)
    y_fuel = b /2*0.55
    
    #fuel weight
    if is_fuel:
        W_fuel_half_wing = 0.3*W_f
    else:
        W_fuel_half_wing = 0
        
    W_fuel_root = 2*W_fuel_half_wing/((1+taper*0.55)*b*0.275)
    Wlst_fuel = W_fuel_root*(1+2/b*(taper-1)*ylst)
    #Wlst_fuel =0 if not fuel in wing 
    #Wlst_fuel = W_fuel_root*(1+2/y_fuel*(taper-1)*ylst) 
    
    #half-wing weight
    W_wing =  40209.08
    W_half_wing = W_wing/2
    W_root = 2*W_wing/((1+taper)*b)
    Wlst = W_root*(1+2/b*(taper-1)*ylst) 

    #Prandtl-Glauert compressibility correction
    M_cr = 0.82
    beta = (1-M_cr**2)**-0.5
    Llst = Cllst*xlst*q_cruise*beta
    Dlst = Cdlst*xlst*q_cruise*beta
    Mlst = Cmlst*xlst**2*q_cruise*beta #pitching moment about c/4 point

    delta_y = (max(ylst)-min(ylst))/len(ylst)

    #total aerodynamic loads
    Ltot = np.sum(Llst*delta_y)
    Dtot = np.sum(Dlst*delta_y)
    Mtot = np.sum(Mlst*delta_y)
    
    #distributed load along span (coordinate system: downward) [N/m], point forces not included yet!
    Fzreslst = -Wlst+Llst -Wlst_fuel*np.heaviside(y_fuel-ylst,1)

    #Freslst = wzreslst*ylst-W_eng*np.heaviside(ylst-y_eng,0.5) #this logically does not mkae sense
    return(Llst,Dlst,Mlst, Fzreslst, Ltot, Dtot, Mtot)

def aero_plots(ylst,Llst,Dlst,Mlst, Fzreslst, Ltot, Dtot, Mtot):
    
    print('Total lift is', Ltot, ' ' ,'Total drag is', Dtot, ' ' , 'Total moment is', Mtot, ' ' ,sep ='\n')
    
    fig, axs = plt.subplots(3, figsize=(8,8), sharex=True)
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
'''
def bending_moment(ylst,Vlst,Fzreslst):
    #wing
    b = 24.63
    
    #engine weight
    m_eng = 3448
    g = 9.80665
    W_eng = m_eng*g
    y_eng = 0.35*b/2
    
    delta_y = (max(ylst)-min(ylst))/len(ylst)
    
    #distributed loads
    #Fzres_tot_sum = np.sum(Fzreslst)*delta_y #Riemann Sum 
    Fzres_tot = simps(Fzreslst, dx=delta_y) #Simpson's Rule 
    
    #testing
    #print(Fzres_tot_sum, Fzres_tot) #negligible differences between Riemann sum and Simpon's Rule
    
    y_res = 1/Fzres_tot*(simps(Fzreslst*ylst, dx=delta_y))
    
    #reaction moment at wing root
    M_x_react = -y_eng*W_eng+y_res*Fzres_tot
    
    #bending moment arrayM_x_react*np.heaviside(ylst,1)
    BMlst = M_x_react*np.heaviside(ylst,1)+cumtrapz(Vlst,initial=0, dx=delta_y)
    
    #testing #works
    #print(M_x_react, Fzres_tot, y_res, Mlst[-1], Mlst[0])
    return(BMlst)


def torsion(ylst, xlst):
    #torsion is taken about c/4 (span axis of lift)
    #torsion along span-axis, at c/4, independent of design condition (depend only on thrust setting)
    
    #wing
    b = 24.63
    #half-wing weight
    W_wing =  40209.08
    W_half_wing = W_wing/2
    taper = 0.4
    b = 24.63
    W_root = 2*W_wing/((1+taper)*b)
    Wlst = W_root*(1+2/b*(taper-1)*ylst) 
    
    #engine 
    m_eng = 3448
    g = 9.80665
    W_eng = m_eng*g
    T_eng = 164600 
    x_eng = 1.122915488 #from c/4 to X_eng #check
    y_eng = 0.35*b/2 
    z_eng = 1.372452263 #check
    
    delta_y = (max(ylst)-min(ylst))/len(ylst)
    
    #torsional loads (y-axis, span-outwards, +ve)
    TMreslst = xlst*(0.5-0.25)*Wlst
    TMres_tot = simps(TMreslst, dx=delta_y) #Simpson's Rule 
    TM_eng = z_eng*T_eng-x_eng*W_eng
    
    #reaction torsion at wing root
    TM_y_react = T_eng+TMres_tot
    
    #torsional moment array-cumtrapz(TMreslst,initial=0, dx=delta_y)+
    TMlst = TM_y_react*np.heaviside(ylst,1)-TMreslst- TM_eng*np.heaviside(ylst-y_eng,1)
    plt.plot(ylst,  TMlst)
    #testing #works
    #print(TM_y_react, TM_eng, TMres_tot,TMlst[-1], TMlst[0])
    return(TMlst)
'''

#lists for aerodynamic coefficients (AOA=0, 10)
xlst_0,ylst_0,Cllst_0, Cdlst_0, Cmlst_0 = aero_coefficient(aero_data_AOA_0)
xlst_10,ylst_10,Cllst_10, Cdlst_10, Cmlst_10 = aero_coefficient(aero_data_AOA_10)

#interpolation of above aero coefficients (AOA=0, 10)
xlst_0,ylst_0,Cllst_0, Cdlst_0, Cmlst_0 = interpolation(xlst_0,ylst_0,Cllst_0, Cdlst_0, Cmlst_0)
xlst_10,ylst_10,Cllst_10, Cdlst_10, Cmlst_10 = interpolation(xlst_10,ylst_10,Cllst_10, Cdlst_10, Cmlst_10)

#add form drag
Cd_0_form = 0.01
Cd_10_form = 0.02
Cdlst_0 += Cd_0_form
Cdlst_0 += Cd_10_form

#design lift coefficient distribution
Cltot_des = 1.1*W_ac/(q_cruise*S_wing)#0.372976647 #not a constant!
Cltot_0 = 0.264851185
Cltot_10 = 1.324255925

#obtain design angle of attack
Cllst_des =  Cllst_0 + (Cltot_des-Cltot_0)/(Cltot_10-Cltot_0)*(Cllst_10-Cllst_0)
alpha_des = np.arcsin((np.sum(Cllst_des)-np.sum(Cllst_0))/(np.sum(Cllst_10)-np.sum(Cllst_0))*np.sin(np.deg2rad(10)))
Cdlst_des = alpha_des/(10-0)*(Cdlst_10-Cdlst_0) +Cd_0_form #added form drag here
Cmlst_des = alpha_des/(10-0)*(Cmlst_10-Cmlst_0)
#print("Design angle of attack is", np.rad2deg(alpha_des)) #testing works

#testing 
#print(Ltot_des*2, Dtot_des*2, Mtot_des*2)

#critical load factors
N_z_positive = 2.5  #change later #done
N_z_negative = -1  #change later #done
N_z_ult = 1.5 #ultimate factor

#lift coefficient during critical load cases
Cltot_des_positive = N_z_positive*Cltot_des
Cltot_des_negative = N_z_negative*Cltot_des


#print(np.sum(Cllst_des*N_z_positive), Cltot_des_positive) #testing #please note that the two values are not the same: 444.9274579865405 and 0.9324416175

#angle of attack during critical load cases
alpha_des_positive = np.arcsin((np.sum(Cllst_des*N_z_positive)-np.sum(Cllst_0))/(np.sum(Cllst_10)-np.sum(Cllst_0))*np.sin(np.deg2rad(10))) #4.3337
alpha_des_negative = np.arcsin((np.sum(Cllst_des*N_z_negative)-np.sum(Cllst_0))/(np.sum(Cllst_10)-np.sum(Cllst_0))*np.sin(np.deg2rad(10))) #-3.4053


#print(np.rad2deg(alpha_des_positive), np.rad2deg(alpha_des_negative)) #testing

#lists for aerodynamic loads (AOA=0, 10)
Llst_0,Dlst_0,Mlst_0, Fzreslst_0,Ltot_0, Dtot_0, Mtot_0 = aero_loads(xlst_0, ylst_0,Cllst_0, Cdlst_0, Cmlst_0)
Llst_10,Dlst_10,Mlst_10, Fzreslst_10, Ltot_10, Dtot_10, Mtot_10 = aero_loads(xlst_10, ylst_10,Cllst_10, Cdlst_10, Cmlst_10)

#lists for aerodynamic loads (desgin point)
Llst_des,Dlst_des,Mlst_des, Fzreslst_des,Ltot_des, Dtot_des, Mtot_des = aero_loads(xlst_0, ylst_0,Cllst_des, Cdlst_des, Cmlst_des)
Llst_poscrit,Dlst_poscrit,Mlst_poscrit, Fzreslst_poscrit,Ltot_poscrit, Dtot_poscrit, Mtot_poscrit = aero_loads(xlst_0, ylst_0,Cllst_des*N_z_positive, Cdlst_des, Cmlst_des) #positive critical load factor
Llst_negcrit,Dlst_negcrit,Mlst_negcrit, Fzreslst_negcrit,Ltot_negcrit, Dtot_negcrit, Mtot_negcrit = aero_loads(xlst_0, ylst_0,Cllst_des*N_z_negative, Cdlst_des, Cmlst_des)  #negatve critical load factor


#adjust the drag (currently only multiplied by laod factor) FIND A BETTER IMPLEMENTATION USING CD/CL CURVE FITTING
Dlst_poscrit  *= N_z_positive    
Dlst_negcrit  *= N_z_negative    

#interpolation of load distribution function
wzresdes_interp = sp.interpolate.interp1d(ylst_0,Fzreslst_des, kind = "cubic", fill_value="extrapolate")



#aerodynamic plots: design and critical conditions (uncomment)
'''
aero_plots(ylst_0, Llst_des, Dlst_des, Mlst_des, Fzreslst_des, Ltot_des, Dtot_des, Mtot_des)
aero_plots(ylst_0, Llst_poscrit,Dlst_poscrit,Mlst_poscrit, Fzreslst_poscrit,Ltot_poscrit, Dtot_poscrit, Mtot_poscrit)
aero_plots(ylst_0, Llst_negcrit,Dlst_negcrit,Mlst_negcrit, Fzreslst_negcrit,Ltot_negcrit, Dtot_negcrit, Mtot_negcrit)
'''

#TMdes = torsion(ylst_0, xlst_0)









#print(Fzresdes_interp) #testing (prints an embedded function, not explicitly algebraic)
#testing
'''
plt.plot(ylst_0,Fzreslst_des)
plt.show()
'''

'''
#testing
b = 24.63
print(len(ylst_0), ylst_0[-1], ylst_0[0], b/2-ylst_0[-1]+ylst_0[0])
'''


#old code: made into functions (SO IGNORE!)
'''
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
'''
'''
fig, axs = plt.subplots(3, figsize=(8,8))
axs[0].plot(ynew,Llst)
axs[0].set_title('Lift')
axs[1].plot(ynew,Dlst)
axs[1].set_title('Drag')
axs[2].plot(ynew, Mlst)
axs[2].set_title('Moment')
plt.show()
'''
'''
ax[2,0].plot(ynew,Mlst)
ax[2,0].set_title('Moment')
plt.show()'''

'''
ax[2,0].plot(ynew,Mlst)
ax[2,0].set_title('Moment')
plt.show()'''

'''
Llst = []
Dlst = []

for i in ylst_0:
    Llst.append(Cl_interp0(i)*x_interp0(i)*q_cruise)
    #Dlst.append(Cd_interp0(i)*x_interp0(i)*q_cruise)
plt.plot(ylst_0,Llst)    #blue line
plt.plot(ylst_0,Dlst)   #orange line
plt.show()
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

#CONSTANT THAT ARE DEFINED GLOBALLY DO NOT NEED TO BE SEPARATELY IMPORTED IN TO FUNCTIONS!!!!!!!

