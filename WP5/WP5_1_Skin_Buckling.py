import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
#from WP4_XFLR5_Raw_Data import *
from WP4_XFLR5_Raw_Data import xlst_0, ylst_0
#from WP4_1_main import *
from WP4_1_main import Vres_poscrit, Vres_negcrit, TMres_poscrit ,TMres_negcrit

# parameters
xlst = xlst_0
ylst = ylst_0

##E = 68.9 * 10 ** 9
##nu = 0.33
##t = 0.004
##h_f = 0.0856 * xlst
##h_r = 0.0542 * xlst
##t_f = 0.004
##t_r = 0.004

#k_c generation
ab_lst_init_B = np.arange(0.75,5.25,0.25)
kc_lst_B_init = [5.6, 5.8, 6.1, 5.5, 5.6, 5.7, 5.5, 5.5, 5.6, 5.5, 5.5, 5.6, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5]

ab_lst_B = np.linspace(min(ab_lst_init_B), max(ab_lst_init_B), num=1000, endpoint=True)
kc_interp_B = sp.interpolate.interp1d(ab_lst_init_B, kc_lst_B_init, kind = "cubic", fill_value="extrapolate")
kc_lst_B = kc_interp_B(ab_lst_B)

# ---


ab_lst_init_C = np.arange(0.75,5.25,0.25)
kc_lst_C_init = [4.4, 4, 4.1, 4.4, 4.2, 4, 4.1, 4.2, 4.1, 4, 4.1, 4.2, 4.1, 4.1, 4.1, 4.1, 4.1, 4.1]

ab_lst_C = np.linspace(min(ab_lst_init_C), max(ab_lst_init_C), num=1000, endpoint=True)
kc_interp_C = sp.interpolate.interp1d(ab_lst_init_C, kc_lst_C_init, kind = "cubic", fill_value="extrapolate")
kc_lst_C = kc_interp_C(ab_lst_C)

# ---

ab_lst_init_E = np.arange(0.75,5.25,0.25)
kc_lst_E_init = [2.2, 1.3, 1, 0.8, 0.8, 0.6, 0.6, 0.6, 0.6, 0.6, 0.5, 0.5, 0.5, 0.5, 0.4, 0.4, 0.4, 0.4]

ab_lst_E = np.linspace(min(ab_lst_init_E), max(ab_lst_init_E), num=1000, endpoint=True)
kc_interp_E = sp.interpolate.interp1d(ab_lst_init_E, kc_lst_E_init, kind = "quadratic", fill_value="extrapolate")
kc_lst_E = kc_interp_E(ab_lst_E)



##clamped_init = [15, 13, 12, 11, 10.5, 10, 9.8, 9.6, 9.8, 9.6, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5]
##clamped_interp = sp.interpolate.interp1d(ab_lst_init, clamped_init, kind = "cubic", fill_value="extrapolate")
##clamped_lst = clamped_interp(ab_lst)


def Sigma_critical(h, n_stringers):
    spacing = 12.35 / (n_stringers + 1)    #first assuming equal stringer spacing, iterate later
    spacing = np.full(1000,spacing)

    a = []
    b = []

    for i in range(len(h)):
        
        if spacing[i] <= h[i]:
            a.append( h[i]) 
            b.append( spacing[i] )

        if spacing[i] >= h[i]:
            b.append( h[i] )
            a.append( spacing[i] )

    a = np.array(a)
    b = np.array(b)
    frac = a / b

    print(frac)
    k_s =  np.interp(frac, ab_lst, ks_lst)
    k_s[0] = np.interp(frac, ab_lst, clamped_lst)[0]

    Sigma_cr =(( np.pi ** 2 * k_s * E ) / ( 12 * ( 1 - nu **2 ) ) ) * ( ( t / b ) ** 2 )

    return Sigma_cr

t_crit_f_4 = Sigma_critical( h_f, 4, )
t_crit_f_12 = Sigma_critical( h_f, 12)
t_crit_f_24 = Sigma_critical( h_f, 24)
t_crit_f_36 = Sigma_critical( h_f, 36)
t_crit_f_60 = Sigma_critical( h_f, 60)
t_crit_f_100 = Sigma_critical( h_f, 100)

t_crit_r_4 = Sigma_critical( h_r, 4, )
t_crit_r_12 = Sigma_critical( h_r, 12)
t_crit_r_24 = Sigma_critical( h_r, 24)
t_crit_r_36 = Sigma_critical( h_r, 36)
t_crit_r_60 = Sigma_critical( h_r, 60)
t_crit_r_100 = Sigma_critical( h_r, 100)













































