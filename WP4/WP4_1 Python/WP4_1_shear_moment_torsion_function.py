# importing tools

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sp
#import sympy as sym
from WP4_XFLR5_Raw_Data import * 
#from WP4_XFLR5_Raw_Data import Vres_des
from WP4_XFLR5_Raw_Data import ylst_0, Llst_des, Fzreslst_des, Ltot_des, q_cruise, Cllst_0, Cdlst_0, is_fuel
from CG_wingboxFRANK import CG_xList, CG_zList

#some constants
g = 9.80665
b = 24.63
Sw_ca = np.arctan( np.tan (25 / 180 * np.pi ) -  ( 0.468 * ( 2 * 4.41 ) / b ) * ( 1 - 0.4 ) )
b_sw = b / np.cos(Sw_ca) #span value in rotated CS
#chords = xlist * np.cos(Sw_ca) #chordlengths in new CS 
 
                      
#fuel weight
W_fuel_tot =  12964*g
#based on ref data, approx. 30% of fuel weight is stored in wing (from root to 0.55/2 spar: consider inner tank only)
y_fuel = b_sw /2*0.55
if is_fuel:
    W_fuel_half_wing = 0.3*W_fuel_tot
else:
    W_fuel_half_wing = 0



def shear( ylst , Llst , Fzreslst , Ltot ):
    ylst = ylst / np.cos(Sw_ca) #correct span for sweep angle
    #wing
    W_wing =  40209.08
    W_half_wing = W_wing/2
    
    #engine weight
    m_eng = 1724 + 393.0809081 #one engine and one nacelle
    W_eng = m_eng * g
    y_eng = 0.35 * b_sw / 2 
    
    #reaction force at wing root
    delta_y = ( max( ylst ) - min( ylst ) ) / len( ylst )
    F_y_react = Ltot - W_half_wing - W_eng - W_fuel_half_wing
    Vlst = - F_y_react * np.heaviside( ylst , 1 ) - W_eng * np.heaviside( ylst - y_eng , 1 ) + np.cumsum( Fzreslst ) * delta_y
 
    #testing #works
    #print('Reaction force is', F_y_react, ' ' ,'Total distributed load is', np.sum(Fzreslst)*delta_y, ' ' , 'Engine weight is', W_eng, ' ' ,sep ='\n')
    #print(Vlst[-1]) #should be close to 0
    return(Vlst)    

# call function 
Vres_des = shear( ylst_0 , Llst_des , Fzreslst_des , Ltot_des )

# bending moment distribution 
def moment( Vlst , ylst ):
    ylst = ylst / np.cos( Sw_ca ) 

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
Mres_des = moment( Vres_des , ylst_0 )

### checking of tip and root values 
##print("reaction moment:", Mres_des[0])
##print("moment at tip:",Mres_des[-1])

#torsion function 
def torsion( xlst , alpha , Llst , Dlst , ylst , CG_xList , CG_zList ):
    xlst = xlst * np.cos( Sw_ac )
    CG_xList = CG_xList * np.cos( Sw_ac )
    ylst = ylst / np.cos ( Sw_ac )
    
    # AOA
    alpha = alpha
    q = q_cruise

    # location ac
    ac_lstx = ( 1 / 4 ) * xlst  #okay like this 

##    plt.plot(ylst_0,ac_lstx)
##    plt.show()

    # location centroid
    xlst_centroid = CG_xList + 0.2 * xlst # !!! CAREFUL with CS !!!! 
    zlst_centroid = CG_zList

    # offset   FINE
    
    dx_lst = xlst_centroid - ac_lstx  
    #dx_lst = np.flip(dx_lst)

##    plt.subplot(3,1,1)
##    plt.plot(ylst,xlst)
##    plt.title("chordlength")
##
##    plt.subplot(3,1,2)
##    plt.plot(ylst,xlst_centroid)
##    plt.title("cg location from LE")
##
##    plt.subplot(3,1,3)
##    plt.plot(ylst,dx_lst)
##    plt.title("Offset")
##    
##    plt.show()

    # normal force
    L_lst = Llst #Cllst * q * xlst
    D_lst = Llst #Cdlst * q * xlst
    N_lst = L_lst * np.cos(alpha) + D_lst * np.sin(alpha)

##    plt.subplot(4,1,1)
##    plt.plot(ylst,Cllst)
##    plt.title("cl")
##
##    plt.subplot(4,1,2)
##    plt.plot(ylst,L_lst)
##    plt.title("lift")
##
##    plt.subplot(4,1,3)
##    plt.plot(ylst,Cdlst)
##    plt.title("Cd")
##
##    plt.subplot(4,1,4)
##    plt.plot(ylst,D_lst)
##    plt.title("Drag")
##    plt.show()


    #resultant moment due to aerodynamic normal force
    Tlst_ad = N_lst * dx_lst

##    plt.plot( ylst , Tlst_ad )
##    plt.show()

    # engine weight and thrust
    m_eng = 3448 + 393.0809081 #one engine and one nacelle
    g = 9.80665
    W_eng = m_eng * g
    Thrust = 154520 #[N]

    # engine offsets from cg 
    x_eng = 2.5 * np.cos( Sw_ca ) # [m] #measured from half chord 
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

    T_lst = sp.integrate.cumtrapz( Tlst_ad , ylst, initial=0) + T_eng * np.heaviside(ylst-y_eng,1) #experiment without integration .
    T_0 = sum(delta_y * Tlst_ad) + T_eng 
    T_lst = T_lst - T_0
    print(T_eng)

    print(T_0)

    return T_lst


T_distr = torsion(xlst_0, 0, Llst_0, Dlst_0, ylst_0, CG_xList, CG_zList)

plt.plot(ylst_0,T_distr)
plt.title(" total Torsion distribution")

plt.show() 



    


    


 





