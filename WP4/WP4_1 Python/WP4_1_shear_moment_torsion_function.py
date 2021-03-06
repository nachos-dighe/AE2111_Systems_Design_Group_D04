# importing tools
import matplotlib.pyplot as plt
import scipy.integrate as sp
#import sympy as sym
from WP4_XFLR5_Raw_Data import * 
#from WP4_XFLR5_Raw_Data import Vres_des
from WP4_XFLR5_Raw_Data import (ylst_0, Llst_des, Fzreslst_des, Ltot_des,
                                q_cruise, Cllst_0, Cdlst_0, is_fuel)
from CG_wingboxFRANK import CG_xList, CG_zList

#some constants
g = 9.80665
b = 24.63
Sw_ca = np.arctan( np.tan (25 / 180 * np.pi ) -  ( ( 0.468 * ( 2 * 4.41 ) / b )
                                                  * ( 1 - 0.4 ) ) )
b_sw = b / np.cos(Sw_ca) #span value in rotated CS
 
                      
#fuel weight
m_pl = 9800
m_oe = 20175
m_mto = 33139
m_f = m_mto - m_oe-m_pl
W_fuel_tot =  m_f*g

#based on ref data, approx. 30% of fuel weight is stored in wing
#(from root to 0.55/2 spar: consider inner tank only)
y_fuel = b_sw / 2 * 0.55
if is_fuel:
    W_fuel_half_wing = 0.3*W_fuel_tot
else:
    W_fuel_half_wing = 0

print('fuel', W_fuel_half_wing)

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
    Vlst = (- F_y_react * np.heaviside( ylst , 1 ) - W_eng *
            np.heaviside( ylst - y_eng , 1 ) + np.cumsum( Fzreslst ) * delta_y)
 
    return(Vlst)    

# call shear function 
Vres_des = shear( ylst_0 , Llst_des , Fzreslst_des , Ltot_des )

# bending moment distribution 
def moment( Vlst , ylst ):
    ylst = ylst / np.cos( Sw_ca ) 

    M_0 = sp.integrate.trapz(Vlst,ylst) #reaction moment
    Mlst = sp.integrate.cumtrapz( Vlst , ylst, initial=0) - M_0

    return Mlst

# call bending moment function 
Mres_des = moment( Vres_des , ylst_0 )

#torsion function 
def torsion( xlst , alpha , Llst , Dlst , ylst , CG_xList , CG_zList ):
    xlst = xlst * np.cos( Sw_ca )
    CG_xList = np.array(CG_xList) * np.cos( Sw_ca )
    ylst = ylst / np.cos ( Sw_ca )
    
    # AOA
    alpha = alpha
    q = q_cruise

    # location ac
    ac_lstx = ( 1 / 4 ) * xlst  #okay like this 

    # location centroid
    xlst_centroid = CG_xList + 0.2 * xlst # !!! CAREFUL with CS !!!! 
    zlst_centroid = CG_zList

    dx_lst = xlst_centroid - ac_lstx  

    # normal force
    L_lst = Llst #Cllst * q * xlst
    D_lst = Dlst * np.cos( Sw_ca ) #Cdlst * q * xlst
    N_lst = L_lst * np.cos(alpha) + D_lst * np.sin(alpha)

    #resultant moment due to aerodynamic normal force
    Tlst_ad = N_lst * dx_lst

    # engine weight and thrust
    m_eng = 3448 + 393.0809081 #one engine and one nacelle
    g = 9.80665
    W_eng = m_eng * g
    Thrust = 82300 #[N]

    # engine offsets from cg 
    x_eng = 2.5 * np.cos( Sw_ca ) # [m] #measured from half chord 
    z_eng = 1.125 # [m]    # measured from chord downwards 
    y_eng = 0.35*b/2 - 2.5 * np.sin( Sw_ca )
    x_half = xlst[285] / 2

    # distance between engine and centroid in x direction 
    dx_eng = x_eng - x_half + 0.2 * xlst[285] + xlst_centroid[285]
    # distance between engine and centroid in z direction
    dz_eng = z_eng - 0.0285 * xlst[285] + zlst_centroid[285] 

    #moments due to engine
    T_w = ( -1 ) * W_eng * dx_eng
    T_thr = Thrust * dz_eng
    T_eng = T_thr + T_w

    #everything together
    delta_y = (max(ylst)-min(ylst))/len(ylst)

    T_lst = ( sp.integrate.cumtrapz( Tlst_ad , ylst, initial=0)
             + T_eng * np.heaviside(ylst-y_eng,1)
             + sp.integrate.cumtrapz(Cmlst_0, ylst, initial=0) )
    T_0 = sum(delta_y * Tlst_ad) + T_eng 
    T_lst = T_lst - T_0
    print(T_eng)

    print(T_0)

    return T_lst

#call torsion function
T_distr = torsion(xlst_0, 0, Llst_0, Dlst_0, ylst_0, CG_xList, CG_zList)


    


    


 





