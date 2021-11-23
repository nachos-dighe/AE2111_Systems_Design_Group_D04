# importing tools

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sp
#import sympy as sym
from WP4_XFLR5_Raw_Data import * 
#from WP4_XFLR5_Raw_Data import Vres_des
from WP4_XFLR5_Raw_Data import ylst_0, Llst_des, Fzreslst_des, Ltot_des
from CG_wingboxFRANK import CG_xList, CG_zList

def shear(ylst,Llst, Fzreslst, Ltot):
    #wing
    b = 24.63
    W_wing =  40209.08
    W_half_wing = W_wing/2
    
    #engine weight
    m_eng = 3448 + 393.0809081 #one engine and one nacelle
    g = 9.80665
    W_eng = m_eng*g
    y_eng = 0.35*b/2
    
    #reaction force at wing root
    delta_y = (max(ylst)-min(ylst))/len(ylst)
    F_y_react = Ltot-W_half_wing-W_eng
    Vlst = -F_y_react*np.heaviside(ylst,1)-W_eng*np.heaviside(ylst-y_eng,1)+np.cumsum(Fzreslst)*delta_y

    #testing #works
    #print('Reaction force is', F_y_react, ' ' ,'Total distributed load is', np.sum(Fzreslst)*delta_y, ' ' , 'Engine weight is', W_eng, ' ' ,sep ='\n')
    #print(Vlst[-1]) #should be close to 0
    return(Vlst)    

# call function 
Vres_des=shear(ylst_0, Llst_des, Fzreslst_des, Ltot_des)

# bending moment distribution 
def moment(Vlst,ylst):

    M_0 = sp.integrate.trapz(Vlst,ylst) #reaction moment
    Mlst = sp.integrate.cumtrapz( Vlst , ylst, initial=0) - M_0 #points of integrated function

    #generate plots 
    '''
    plt.plot(ylst,Mlst)
    plt.title('Moment diagram')
    plt.xlabel('Spanwise position')
    plt.ylabel('Bending moment')
    plt.show()
    '''
    return Mlst

# call function 
Mres_des=moment(Vres_des,ylst_0)

# checking of tip and root values 
print("reaction moment:", Mres_des[0])
print("moment at tip:",Mres_des[-1])

#torsion function 
def torsion(xlst, alpha, Cl_lst, Cd_lst, ylst, CG_xList, CG_zList):
    # AOA
    alpha = alpha
    v_cruise = 243.13
    rho_cruise = 0.37956
    q_lst = ( 1 / 2 ) * rho_cruise * v_cruise ** 2
    b = 24.63

    # location ac
    ac_lstx = ( 1 / 4 ) * xlst 

    # location centroid
    xlst_centroid = CG_xList  # !!! CAREFUL with CS !!!! 
    zlst_centroid = CG_zList

    # offset
    dx_lst = xlst_centroid - ac_lstx

    # normal force
    Cn_lst = Cl_lst * np.cos(alpha) + Cd_lst * np.sin(alpha)
    N_lst = Cn_lst * xlst * q 

    #resultant moment due to aerodynamic normal force
    Tlst_ad = N_lst * dx_lst

    # engine weight and thrust
    m_eng = 3448 + 393.0809081 #one engine and one nacelle
    g = 9.80665
    W_eng = m_eng*g
    Thrust = 154520 #[N]

    # engine offsets from cg 
    x_eng = 2.5 # [m] #measured from half chord 
    z_eng = 1.125 # [m]    # measured from chord downwards 
    y_eng = 0.35*b/2
    x_half = xlst[350] / 2 

    dx_eng = x_eng - x_c/2 + 0.2 * xlst[350] + xlst_centroid[350] # distance between engine and centroid in x direction 
    dz_eng = z_eng - 0.0285 * xlst[350] + zlst_centroid[350] # distance between engine and centroid in z direction

    #moments due to engine
    T_thr = T_eng * dz_eng
    T_w = ( -1 ) * W_eng * dx_eng
    T_eng = T_thr + T_w

    #everything together
    delta_y = (max(ylst)-min(ylst))/len(ylst)
    T_lst = np.cumsum(Tlst_ad) * delta_y + T_eng * np.heaviside(ylst-y_eng,1) # add internal moment ?

    return T_lst


T_distr = torsion(xlst_0, 0, Cllst_0, Cdlst_0, ylst_0, CG_xList, CG_zList)

plt.plot(T_distr,ylst_0)
plt.title("Torsion distribution")
plt.xlabel("Spanwise location")
plt.ylabel("Torsion")
plt.show() 


    

""""
# torsion distribution

def torsion(ylst, Llst, xlst, Ltot):
    # chord
    dlst = ( 1 / 4 ) * xlst # checked and okay

    # wing
    b = 24.63
    W_wing =  40209.08
    W_half_wing = W_wing/2

    #engine weight        # checked and okay 
    m_eng = 3448 #[Kg]
    g = 9.80665
    W_eng = m_eng*g # [N]
    y_eng = 0.35*b/2
    
    #engine Thrust          
    Teng = 154520 # [N] 

    # engine offset
    x_eng = 2.5 # [m]
    z_eng = 1.125 # [m]

    #Torsion due to engine weight    # checked and okay 
    T_w = W_eng * x_eng * (-1)
    print('Torsion due to engine weight:',T_w)

    #Torsion due to thrust     # checked and okay 
    T_t = Teng * z_eng
    print('Torsion due to thrust:',T_t)

    # Torsion due to lift
    t_l = Llst * dlst # distributed torque due to lift
    plt.plot(ylst,t_l)
    plt.show()
    
    t_ltot = sp.integrate.trapz(t_l,ylst) #total torque due to lift 
    print('Torsion due to lift:',t_l, 'and in total:',t_ltot)
    print(Ltot)

    # reaction torque
    T_r =( t_ltot + T_w + T_t ) * (-1)
    print('reaction torque:',T_r)

    # distribution
    Tlst = T_r + T_t * np.heaviside(ylst - y_eng, 1)- T_w * np.heaviside(ylst - y_eng, 1 ) + t_l

    #plotting
    '''
    plt.plot(ylst,Tlst)
    plt.title('Torsion distribution')
    plt.xlabel('Spanwise position [m]')
    plt.ylabel('Torsion [Nm]')
    plt.show()
    '''
    return Tlst 

Tres_des = torsion(ylst_0, Llst_des, xlst_0, Ltot_0)
"""


 





