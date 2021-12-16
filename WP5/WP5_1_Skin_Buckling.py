import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
#from WP4_XFLR5_Raw_Data import *
from WP4_XFLR5_Raw_Data import xlst_0, ylst_0
#from WP4_1_main import *
from WP4_1_main import Vres_poscrit, Vres_negcrit, TMres_poscrit ,TMres_negcrit
import WP5_2_Chord_LengthFRANK as Lengths
import WP5_2_MOI_FRANK as Moi_Box

# Rewriting parameters
xlst = xlst_0
ylst = ylst_0

# Material properties and dimensions
E = 68.9 * 10 ** 9
nu = 0.33
t = 0.004
h_f = 0.0856 * xlst # !! Look if this is correct
h_r = 0.0542 * xlst # !! Look if this is correct
t_f = 0.004 # !! assumed thickness
t_r = 0.004 # !! assumed thickness

RCr = 4.4 # [m] Root chord
TCr = 1.76 # [m] Tip chord
Span = 24.64 # [m] Span

# Counters
i = 0

# Calcaulting the dimensions of the wingbox
alpha, beta, b2, DeltaX, Cr = Lengths.WingboxDimensions(RCr, TCr, Span, ylst_0)
print(Cr)
# Defining the lists to stroe values
Stress_Top_List = []
Stress_Bottom_List = []

# --------------------------------------------------------------------
# Reading the moment stress from the file

with open("Normal_Stress_Top_Panel.dat", "r") as file : # Reads the y position file 
    Stress_Top_RAW = file.readlines()

for line in Stress_Top_RAW :
    Stress_Top = line.replace("\n", "")
    Stress_Top = float(Stress_Top)
    Stress_Top_List.append(Stress_Top)


with open("Normal_Stress_Bottom_Panel.dat", "r") as file : # Reads the y position file 
    Stress_Bottom_RAW = file.readlines()

for line in Stress_Bottom_RAW :
    Stress_Bottom = line.replace("\n", "")
    Stress_Bottom = float(Stress_Bottom)
    Stress_Bottom_List.append(Stress_Bottom)
   
# --------------------------------------------------------------------
# Interpolation the graphs that are in the appendix of the reader

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

##plt.plot(ab_lst_C, kc_lst_C)
##plt.show()
# --------------------------------------------------------------------
# Making the function to calculate everything

def Sigma_critical(h, n_stringers):
    spacing = 12.35 / (n_stringers + 1)    #first assuming equal stringer spacing, iterate later
    spacing = np.full(1000,spacing)

    a = []
    b = []
    n_ribs = 40 #!! Don't know
    Span = 12.35 #!! check


    for i in range(len(h)):
        b.append(Cr[i]/n_stringers)
        a.append((Span/2)/n_ribs)
        

    a = np.array(a)
    b = np.array(b)
    frac = a / b

    print(frac)
    k_c =  np.interp(frac, ab_lst_C, kc_lst_C)
    k_c[0] = np.interp(frac, ab_lst_B, kc_lst_B)[0]
    k_c[999] = np.interp(frac, ab_lst_E, kc_lst_E)[999]

    Sigma_cr =(( np.pi ** 2 * k_c * E ) / ( 12 * ( 1 - nu **2 ) ) ) * ( ( t / b ) ** 2 )
    
    print("a", a)
    print("b", b)
    print("frac", a/b)
    print("k_c", k_c)
    return Sigma_cr


def Sigma_Requeird(M, Cr) : # NOT USED
    c = 0.5* b2 + np.tan(alpha) * DeltaX
    CG_Z = 0.038 * Cr
    #CG_X = 0.268 * Cr
    I = Moi_Box.Ixx_wingbox(DeltaX,beta,alpha,CG_Z,t, b)
    Sigma_max = (M * c) / I
    return Sigma_max

i = 0
while i <= 999 :
    Stress_Bottom_List[i] = abs(Stress_Bottom_List[i])
    i = i +1
# --------------------------------------------------------------------
# Calling the fucntions and plotting the result

Sig_crit_f_1 = Sigma_critical( h_f, 1)
Sig_crit_f_2 = Sigma_critical( h_f, 2)
Sig_crit_f_3 = Sigma_critical( h_f, 3)
Sig_crit_f_4 = Sigma_critical( h_f, 4)
 
##while i <= 999 :
##    Sigma_max = Sigma_Requeird(M, Cr[i])
##    i = i +1
plt.plot(ylst, Stress_Top_List)
plt.plot(ylst, Stress_Bottom_List)
plt.plot(ylst, Sig_crit_f_1)
plt.plot(ylst, Sig_crit_f_2)
plt.plot(ylst, Sig_crit_f_3)
plt.plot(ylst, Sig_crit_f_4)
plt.title("Different stringer configurations")
plt.legend(['Sigma max Top', 'Sigma max Bottom', '1 stringer', '2 stringers', '3 stringers', '4 stringers'], loc='upper right')

plt.show()



# needs to be done:
# [ ] Put Max load in to the code
# [V] Make graph titles
# [ ] Ask what the ribs pacing is
# [ ] Tidy up the code
# [ ] Check code





































