# importing tools

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sp
import sympy as sym
from WP4_XFLR5_Raw_Data import Vres_des
from WP4_XFLR5_Raw_Data import ylst_0


# bending moment distribution 
def moment(Vlst,ylst):

    M_0 = sp.trapz(Vlst,ylst) #reaction moment
    Mlst = sp.cumtrapz( Vlst , ylst, initial=0) - M_0 #points of integrated function

    #generate plots 
    plt.plot(ylst,Mlst)
    plt.title('Moment diagram')
    plt.xlabel('Spanwise position')
    plt.ylabel('Bending moment')
    plt.show()

    return Mlst


Mres_des=moment(Vres_des,ylst_0)




print("shearist:",Vres_des)
print("reaction moment:", Mres_des[0])
print("moment at tip:",Mres_des[-1])




 





