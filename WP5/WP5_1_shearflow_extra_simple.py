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
t = 0.004
h_f = 0.0856 * xlst
h_r = 0.0542 * xlst
t_f = 0.004
t_r = 0.004

#k_s generation
ab_lst_init = np.arange(1,5.25,0.25)
ks_lst_init = [9.4, 8, 7.1, 6.6, 6.4, 6.2, 6.1, 6, 5.8, 5.7, 5.8, 5.9, \
               5.7, 5.6, 5.6, 5.5, 5.5]
ab_lst = np.linspace(min(ab_lst_init), max(ab_lst_init), num=1000,\
                     endpoint=True)
ks_interp = sp.interpolate.interp1d(ab_lst_init, ks_lst_init, kind \
                                    = "cubic", fill_value="extrapolate")
ks_lst = ks_interp(ab_lst)
clamped_init = [15, 13, 12, 11, 10.5, 10, 9.8, 9.6, 9.8, 9.6, 9.5, 9.5,\
                9.5, 9.5, 9.5, 9.5, 9.5]
clamped_interp = sp.interpolate.interp1d(ab_lst_init, clamped_init, kind \
                                         = "cubic", fill_value="extrapolate")
clamped_lst = clamped_interp(ab_lst)

# shear flow due to shear
def shearstress_ave (Vlst, t_f, t_r ):
    tau_av_lst = Vlst / ( 0.0865 * xlst * t_f + 0.0542 * xlst * t_r)
    return tau_av_lst

def shearstress_T (t, Tlst):
    q = Tlst / ( ( 0.0856 * xlst + 0.0542 * xlst ) * 0.55 * xlst )
    tau_T = q / t
    return tau_T

# calculator for number of ribs and their locations 
def rib_calc(tau_appl):
    ribs = [0]
    ribs_index = [0]

    for i in range(1,len(ylst)):

        b = ylst[i] - ribs[-1]
        height = h_f[ribs_index[-1]]
        small = []
        large = []

        if b >= height:
            L = b
            large.append(L)
            S = height
            small.append(S)
        if b <= height:
            L = height
            large.append(L)
            S = b
            small.append(S)
        frac = L/S
        k_s =  np.interp(frac, ab_lst, ks_lst)
        

        tau_crit = (( np.pi ** 2 * k_s * E ) / ( 12 * ( 1 - nu**2 ) ) ) \
                   * ( ( t / S ) ** 2 )

        if tau_crit <= tau_appl[i] * 1.03:
            ribs.append(ylst[i-1])
            ribs_index.append(i)
    ribs.append(ylst[-1])
    ribs_index.append(len(ylst))

    return ribs,ribs_index, small, large

def margins(appl, crit):
    marg = crit/appl
    return marg

#call functions
tau_tot_f_pos = np.absolute(shearstress_ave(Vres_poscrit, t_f, t_r) \
                            * 1.5 + shearstress_T(t_f, TMres_poscrit))
tau_tot_r_pos = np.absolute(shearstress_ave(Vres_poscrit, t_f, t_r) \
                            * 1.5 - shearstress_T(t_f, TMres_poscrit))
tau_tot_f_neg = np.absolute(shearstress_ave(Vres_negcrit, t_f, t_r) \
                            * 1.5 + shearstress_T(t_f, TMres_negcrit))
tau_tot_r_neg = np.absolute(shearstress_ave(Vres_negcrit, t_f, t_r) \
                            * 1.5 - shearstress_T(t_f, TMres_negcrit))

#spacing list 
ribs, indices, small, large = rib_calc(tau_tot_f_pos)
newlist = []
spacing = []
spacing = []
for i in range(len(ribs)-1):
    spacing.append(ribs[i+1]-ribs[i])
for i in range(len(indices)-1):
    k = indices[i+1] - indices[i]
    temp = np.full(k,spacing[i-1])
    temp_lst = list(temp)
    newlist.extend(temp_lst)

# critical buckling plot
checklist = []

for i in range(len(ylst)):
    b = newlist[i]
    height = h_f[i]
    if b >= height:
        large = b
        small = height
    if b <= height:
        large = height
        small = b

    frac = large/small
    k_s =  np.interp(frac, ab_lst, ks_lst)   
    tau_cr =(( np.pi ** 2 * k_s * E ) / ( 12 * ( 1 - nu ** 2) )) \
             * ( ( t / small ) ** 2 )
    checklist.append(tau_cr)

#calling margin functions 
marg_f_pos = margins(tau_tot_f_pos,checklist)
marg_r_pos = margins(tau_tot_r_pos,checklist)
marg_f_neg = margins(tau_tot_f_neg,checklist)
marg_r_neg = margins(tau_tot_r_neg,checklist)


