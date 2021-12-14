import numpy as np
import matplotlib.pyplot as plt
from WP4_XFLR5_Raw_Data import xlst_0, ylst_0


#type stringer: (0,1) = (I, L) for #I,L stringer respectively
def column_buckling(n_stringer, type_stringer, Astringer_lst, t):
    E = 68.9 * 10 ** 9
    L = 24.63 / 2  # half-span (w.o. coordinate transformation)
    K = 1 / 4  # K= (1/4) one fixed, one free end  #K = 4 one fixed, one free end
    sigma_yield = 241 * 10 ** 6  # compressive strengh of Aluminum, incorrect approach (refine later)
    Sf = 1.5 #safety factor
    sigma_allow = sigma_yield/Sf

    if type_stringer ==0:
        alst = (Astringer_lst/t)/4.1 #based on optimised design
        blst = alst
        clst = 2.1*alst
        yclst = (alst*blst+blst*blst/2)/(alst+blst+clst)
        Iminlst =((blst-yclst)**2*alst+yclst**2*clst+(blst/2-yclst)**2*blst+blst**3/12) #Ixx/t= Imin/t [m^3]
    elif type_stringer ==1:
        alst =  (Astringer_lst/t)/2 #based on optimised design
        blst = alst
        yclst = alst/4 #xclst = yclst
        Iminlst = (yclst** 2 * alst + alst** 3 / 12 + (alst / 2 - yclst)** 2 * alst) #Ixx/t = Iyy/t =Imin/t [m^3]

    sigma_crit_lst = (K*np.pi**2*E*Iminlst)/(L**2*Astringer_lst)
    print(Iminlst[-1], sigma_crit_lst[-1])
    #sigma_crit_lst /= n_stringer  # assume stress equally divided across stringers #PLEASE RE-CHECK, NOT SURE
    MOS_lst = sigma_crit_lst/sigma_allow
    '''
    c_xx = 5 / 24  # I_xx = c_w_stringer**3*t #dependent on shape. Currently L-shaped stringer.
    c_yy = 5 / 24  # I_yy = w_stringer**3*t #dependent on shape. Currently L-shaped stringer.
    c = min(c_xx, c_yy)
    w_stringer = np.sqrt((2 * sigma_cr * L ** 2) / (c * K * np.pi ** 2 * E))
    '''
    return (MOS_lst)

#initialisation
A_stringer_root = 0.0003 #assumed [m]
A_stringer_tip = 0.0003 #assumed [m]
Astringer_lst=np.linspace(A_stringer_root, A_stringer_tip,len(ylst_0))
t_stringer = 0.001 #assumed [m] #const thickness

MOS_lst_4L_stringer = column_buckling(4, 1, Astringer_lst, t_stringer)

#plots
plt.plot(ylst_0, MOS_lst_4L_stringer)
plt.show()





'''
w_stringer = column_buckling(3)
print(w_stringer)  # testing
'''

