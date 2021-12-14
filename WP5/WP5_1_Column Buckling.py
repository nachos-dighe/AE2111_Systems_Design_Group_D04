import numpy as np
import matplotlib.pyplot as plt
from WP4_XFLR5_Raw_Data import xlst_0, ylst_0
from WP4_1_main import BMres_poscrit, BMres_negcrit

#wingbox dimensions (z from centroidal x-axis)
alpha = np.deg2rad(2.54)
beta = np.deg2rad(0.73)
DeltaX = 0.55*xlst_0

z_LE = 0.0856*xlst_0
z_TE = 0.0542*xlst_0 #b

z_LE_bottom = 0.038*xlst_0
z_TE_bottom = z_LE_bottom-DeltaX*np.tan(beta)

z_LE_top = z_LE-z_LE_bottom
z_TE_top = z_LE-z_LE_bottom-DeltaX*np.tan(alpha)

def MOI_calculator(DeltaX, beta, alpha, z, b):
    Ixx1 = ((((DeltaX) ** 3) * ((np.sin(beta)) ** 2)) / (12 * ((np.cos(beta)) ** 3))) + ((DeltaX) / np.cos(beta)) * (
                z - ((DeltaX * np.tan(beta)) / 2)) ** 2  # lower left angled profile

    Ixx2 = (((DeltaX) ** 3) * ((np.sin((alpha)) ** 2)) / (12 * ((np.cos(alpha)) ** 3))) + (DeltaX / (np.cos(alpha))) * (
                (-DeltaX * np.tan(beta)) - b - ((DeltaX * np.tan(alpha)) / 2) + z) ** 2  # upper right angled profile

    Ixx3 = 1 / 12 * ((DeltaX * np.tan(beta) + b + DeltaX * np.tan(alpha)) ** 3) + (
                DeltaX * np.tan(beta) + b + DeltaX * np.tan(alpha)) * (
                       z - ((DeltaX * np.tan(beta) + b + DeltaX * np.tan(alpha)) / 2)) ** 2  # vertical profile on the left

    Ixx4 = 1 / 12 * b ** 3 + b * (DeltaX * np.tan(beta) + (b / 2) - z) ** 2  # vertical profile on the right

    Ixx = Ixx1 + Ixx2 + Ixx3 + Ixx4
    return Ixx

#I_wb =((((DeltaX)**3)*((sin(beta))**2))/(12*((cos(beta))**3)))+((DeltaX)/cos(beta))*(z-((DeltaX * tan(beta))/2))**2 + (((DeltaX)**3)*((sin((alpha))**2))/(12*((cos(alpha))**3)))+(DeltaX/(cos(alpha)))*((-DeltaX*tan(beta))-b-((DeltaX*tan(alpha))/2)+z)**2 + 1/12 * ((DeltaX*tan(beta)+b+DeltaX*tan(alpha))**3) +(DeltaX*tan(beta)+b+DeltaX*tan(alpha))*(z-((DeltaX*tan(beta)+b+DeltaX*tan(alpha))/2))**2 + 1/12 * b**3 + b*(DeltaX*tan(beta)+(b/2)-z)**2
#I_wb/t = ((0.0856*xlst_0)**3+(0.268*xlst_0)**2*0.0856*xlst_0)+((0.0856*xlst_0)**3+(0.268*xlst_0)**2*0.0856*xlst_0)
#z_wbbottom_lst = np.linspace(z_LE_bottom, z_TE_bottom, n_stringer, endpoint=True)
#z_wbtop_lst = np.linspace(z_LE_top, z_TE_top, n_stringer, endpoint=True)

#type stringer: (0,1) = (I, L) for #I,L stringer respectively
def column_buckling(z_LE_0, z_TE_0, I_wb, BM, n_stringer, type_stringer_lst, Astringer_lst, t):  #z_LE_0,z_TE_0  (0: can be replaced with top/bottom), BM: pos/neg crit,

    #stringer material/geometry
    E = 68.9 * 10 ** 9
    L = 24.63 / 2  # half-span (w.o. coordinate transformation)
    K = 1 / 4  # K= (1/4) one fixed, one free end  #K = 4 one fixed, one free end
    #sigma_yield = 241 * 10 ** 6  # compressive strengh of Aluminum, incorrect approach (refine later)
    Sf = 1.5 #safety factor

    #stringer applied stress:
    zlst = np.linspace(z_LE_0, z_TE_0, n_stringer, endpoint=True)
    sigma_allow_lst = np.empty([n_stringer, len(BM)])
    MOS_lst_lst = np.empty([n_stringer, len(BM)])

    for i in range(0, n_stringer):
        #allowable stress
        sigma_allow= BM*I_wb/zlst[i]*Sf
        sigma_allow_lst[i, :] = sigma_allow

        if type_stringer_lst[i] ==0: #I-stringer
            alst = (Astringer_lst/t)/4.1 #based on optimised design
            blst = alst
            clst = 2.1*alst
            yclst = (alst*blst+blst*blst/2)/(alst+blst+clst)
            Iminlst =((blst-yclst)**2*alst+yclst**2*clst+(blst/2-yclst)**2*blst+blst**3/12) #Ixx/t= Imin/t [m^3]
        elif type_stringer_lst[i] ==1: #L-stringer
            alst =  (Astringer_lst/t)/2 #based on optimised design
            blst = alst
            yclst = alst/4 #xclst = yclst
            Iminlst = (yclst** 2 * alst + alst** 3 / 12 + (alst / 2 - yclst)** 2 * alst) #Ixx/t = Iyy/t =Imin/t [m^3]

        #failure stress
        sigma_crit_lst = (K*np.pi**2*E*Iminlst)/(L**2*Astringer_lst)

        #print(Iminlst[-1], sigma_crit_lst[-1]) #testing #works
        #sigma_crit_lst /= n_stringer  # assume stress equally divided across stringers #INCORRECT

        #margin of safety for ith stringer, spanwise
        MOS_lst = sigma_crit_lst/sigma_allow
        #margin of safety for all stringers, spanwise
        MOS_lst_lst[i, :] = MOS_lst
        #MOS_lst_lst = np.append(MOS_lst_lst, MOS_lst, axis=1)

    '''
    c_xx = 5 / 24  # I_xx = c_w_stringer**3*t #dependent on shape. Currently L-shaped stringer.
    c_yy = 5 / 24  # I_yy = w_stringer**3*t #dependent on shape. Currently L-shaped stringer.
    c = min(c_xx, c_yy)
    w_stringer = np.sqrt((2 * sigma_cr * L ** 2) / (c * K * np.pi ** 2 * E))
    '''
    return (MOS_lst_lst, sigma_allow_lst)

#initialisation (area stringer)
A_stringer_root = 0.0003 #assumed [m]
A_stringer_tip = 0.0003 #assumed [m]
Astringer_lst=np.linspace(A_stringer_root, A_stringer_tip,len(ylst_0))
t_stringer = 0.001 #assumed [m] #const thickness

#initialisation (stringer instances)
n_stringer_top = 4 #can be changed
n_stringer_bottom = 3 #can be changed
type_stringer_lst_top = np.array([1,0,0,1]) #0: I-stringer; 1: L-stringer (come up with better implementation)
type_stringer_lst_bottom = np.array([1,0,1]) #0: I-stringer; 1: L-stringer (come up with better implementation)

#calculate MOI of WB (w/o stringer)
I_wb = MOI_calculator(DeltaX, beta, alpha, z_LE_bottom, z_TE)

#spanwise margin of safety
MOS_lst_lst_top, sigma_allow_top_lst = column_buckling(z_LE_top, z_TE_top, I_wb, BMres_poscrit, n_stringer_top, type_stringer_lst_top, Astringer_lst, t_stringer)
MOS_lst_lst_bottom, sigma_allow_bottom_lst = column_buckling(z_LE_bottom, z_TE_bottom, I_wb, BMres_negcrit, n_stringer_bottom, type_stringer_lst_bottom, Astringer_lst, t_stringer)

save_input = int(input('To save the bending stress files as .txt, input 1 '))
if save_input == 1:
    np.savetxt('Normal_Stress_Top_Panel.txt', sigma_allow_top_lst[0], delimiter='\\')
    np.savetxt('Normal_Stress_Bottom_Panel.txt',sigma_allow_bottom_lst[0], delimiter='\\')


#plots\
'''
plt.plot(ylst_0, MOS_lst_4L_stringer)
plt.show()
'''

'''
w_stringer = column_buckling(3)
print(w_stringer)  # testing
'''

