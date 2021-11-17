# importing tools

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sp
import sympy as sym
from WP4_XFLR5_Raw_Data import * 
from WP4_XFLR5_Raw_Data import Vres_des
from WP4_XFLR5_Raw_Data import ylst_0


# bending moment distribution 
def moment(Vlst,ylst):

    M_0 = sp.integrate.trapz(Vlst,ylst) #reaction moment
    Mlst = sp.integrate.cumtrapz( Vlst , ylst, initial=0) - M_0 #points of integrated function

    #generate plots 
    plt.plot(ylst,Mlst)
    plt.title('Moment diagram')
    plt.xlabel('Spanwise position')
    plt.ylabel('Bending moment')
    plt.show()

    return Mlst

# call function 
Mres_des=moment(Vres_des,ylst_0)

# checking of tip and root values 
print("reaction moment:", Mres_des[0])
print("moment at tip:",Mres_des[-1])


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
    Tlst = T_r * np.heaviside(ylst,1) + T_t * np.heaviside(ylst - y_eng, 1)- T_w * np.heaviside(ylst - y_eng, 1 ) + t_l

    #plotting
    plt.plot(ylst,Tlst)
    plt.title('Torsion distribution')
    plt.xlabel('Spanwise position [m]')
    plt.ylabel('Torsion [Nm]')
    plt.show()
    
    return Tlst 

Tres_des = torsion(ylst_0, Llst_des, xlst_0, Ltot_0)


 





