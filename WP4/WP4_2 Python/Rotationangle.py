#Defining the functions for returning the rotation

import ylst
import scipy.integrate as sp
import numpy as np
from matplotlib import pyplot as plt


def rotation(T_lst, J_lst, ylst):

    num = J_lst
    frac = [i / j for i, j in zip(T_lst, num)]
    rot_lst = sp.cumtrapz(frac,ylst,initial=0)

    return rot_lst


##rot_lst = rotation(T_lst, J_lst, G, ylst0)
##print(rot_lst)

##plt.plot(rot_lst, ylst0, 'rs-', label='Deflection')
##plt.axhline(0, color="black")
##plt.axvline(0, color="black")
##plt.legend()
##plt.grid()
##plt.show()

