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

E = 68.9 * 10 ** 9
nu = 0.33
t = 0.00198
h_f = 0.0856 * xlst
h_r = 0.0542 * xlst
t_f = 0.00198
t_r = 0.00198

#k_s generation
ab_lst_init = np.arange(1,5.25,0.25)
ks_lst_init = [9.4, 8, 7.1, 6.6, 6.4, 6.2, 6.1, 6, 5.8, 5.7, 5.8, 5.9, 5.7, 5.6, 5.6, 5.5, 5.5]
ab_lst = np.linspace(min(ab_lst_init), max(ab_lst_init), num=1000, endpoint=True)
ks_interp = sp.interpolate.interp1d(ab_lst_init, ks_lst_init, kind = "cubic", fill_value="extrapolate")
ks_lst = ks_interp(ab_lst)



def tau_critical(h, n_ribs):
    spacing = 12.35 / (n_ribs + 1)    #first assuming equal rib spacing, iterate later
    spacing = np.full(1000,spacing)

    a = []
    b = []

    for i in range(len(h)):
        
        if spacing[i] <= h[i]:
            a.append(h[i]) 
            b.append( spacing[i] )

        if spacing[i] >= h[i]:
            b.append( h[i] )
            a.append( spacing[i] )

    a = np.array(a)
    b = np.array(b)
    frac = a / b

    print(frac)
    k_s = np.interp(frac, ab_lst, ks_lst) 

    tau_cr =(( np.pi ** 2 * k_s * E ) / ( 12 * ( 1 - nu ) ** 2 ) ) * ( ( t / b ) ** 2 )

    return tau_cr

t_crit_f_4 = tau_critical( h_f, 4)
t_crit_f_12 = tau_critical( h_f, 12)
t_crit_f_24 = tau_critical( h_f, 24)
t_crit_f_36 = tau_critical( h_f, 36)
t_crit_f_100 = tau_critical( h_f, 100)
t_crit_r = tau_critical( h_r, 12)


# shear flow due to shear   # tau_av = V / ( h_f * t_f + h_r * t_r )
# ==> multipy with appropriate k_v
# ==> multiply with saftey factor

def shearstress_ave (Vlst, t_f, t_r ):
    tau_av_lst = Vlst / ( 0.0865 * xlst * t_f + 0.0542 * xlst * t_r)
    return tau_av_lst

def shearstress_T (t, Tlst):
    q = Tlst / ( ( 0.0856 * xlst + 0.0542 * xlst ) * 0.55 * xlst )
    tau_T = q / t
    return tau_T

#call functions 

tau_tot_f_pos = shearstress_ave(Vres_poscrit, t_f, t_r) * 1.5 + shearstress_T(t_f, TMres_poscrit)
tau_tot_r_pos = shearstress_ave(Vres_poscrit, t_f, t_r) * 1.5 - shearstress_T(t_f, TMres_poscrit)

tau_tot_f_neg = shearstress_ave(Vres_negcrit, t_f, t_r) * 1.5 + shearstress_T(t_f, TMres_negcrit)
tau_tot_r_neg = shearstress_ave(Vres_negcrit, t_f, t_r) * 1.5 - shearstress_T(t_f, TMres_negcrit)

#plotting
plt.subplot(4,1,1)
plt.plot(ylst, tau_tot_f_pos)
plt.plot(ylst, t_crit_f_24)
plt.title("positive loadcase front spar")

plt.subplot(4,1,2)
plt.plot(ylst, tau_tot_r_pos)
plt.plot(ylst, t_crit_r)
plt.title("positive loadcase rear spar")

plt.subplot(4,1,3)
plt.plot(ylst, tau_tot_f_neg)
plt.plot(ylst, t_crit_f_4)
plt.plot(ylst,t_crit_f_12)
plt.plot(ylst,t_crit_f_24)
plt.plot(ylst,t_crit_f_36)
plt.plot(ylst,t_crit_f_100)

plt.legend(['tau max','4 ribs', '12 ribs', '24 ribs', '36 ribs'], loc='upper left')
plt.title("negative loadcase front spar")

plt.subplot(4,1,4)
plt.plot(ylst, tau_tot_r_neg)
plt.plot(ylst, t_crit_r)
plt.title("negative loadcase rear spar")

plt.show()









