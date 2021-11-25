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
def torsion(xlst, alpha, L_lst, D_lst, ylst, CG_xList, CG_zList):
    # AOA
    alpha = alpha
    v_cruise = 243.13
    rho_cruise = 0.37956
    q_lst = ( 1 / 2 ) * rho_cruise * v_cruise ** 2
    b = 24.63
    span_rev = ylst * (-1) 

    # location ac
    ac_lstx = ( 1 / 4 ) * xlst  #okay like this 

##    plt.plot(ylst_0,ac_lstx)
##    plt.show()

    # location centroid
    xlst_centroid = CG_xList  # !!! CAREFUL with CS !!!! 
    zlst_centroid = CG_zList

    # offset
    
    dx_lst = xlst_centroid - ac_lstx # - ac_lstx
    dx_lst = np.flip(dx_lst)
    plt.plot(ylst_0,dx_lst)
    plt.show()

    # normal force
    N_lst = L_lst * np.cos(alpha) + D_lst * np.sin(alpha)
    #N_lst = Cn_lst * xlst * q_lst


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

    dx_eng = x_eng - x_half + 0.2 * xlst[350] + xlst_centroid[350] # distance between engine and centroid in x direction 
    dz_eng = z_eng - 0.0285 * xlst[350] + zlst_centroid[350] # distance between engine and centroid in z direction

    #moments due to engine
    T_w = ( -1 ) * W_eng * dx_eng
    T_thr = Thrust * dz_eng
    T_eng = T_thr + T_w

    #everything together
    delta_y = (max(ylst)-min(ylst))/len(ylst)
    #T_lst = np.cumsum(Tlst_ad) * delta_y + T_eng * np.heaviside(ylst-y_eng,1) # add internal moment ?
    T_lst = Tlst_ad + T_eng * np.heaviside(ylst-y_eng,1) #experiment without integration . 

    return T_lst, N_lst, Tlst_ad, dx_lst


T_distr, Nlst, T_ad, dxlist = torsion(xlst_0, 0, Llst_0, Dlst_0, ylst_0, CG_xList, CG_zList)


plt.subplot(4,1,1)
plt.plot(ylst_0,T_distr)
plt.title(" total Torsion distribution")

plt.subplot(4,1,2)
plt.plot(ylst_0,Nlst)
plt.title("Spanwise normal force")

plt.subplot(4,1,3)
plt.plot(ylst_0,T_ad)
plt.title("Torsion due to ad forces spanwise")

plt.subplot(4,1,4)
plt.plot(ylst_0, dxlist)
plt.title("Spanwise momentarm") 


plt.show() 



    


    


 





