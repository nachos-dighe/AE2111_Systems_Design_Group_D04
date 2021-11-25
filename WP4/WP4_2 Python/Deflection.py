#Defining the functions for returning the deflection

import ylst
import scipy.integrate as sp
import numpy as np
from matplotlib import pyplot as plt
ylst0 = [1,2,3,4,5]
M_lst = [1,2,3,4,5]
I_lst = [2,4,6,8,10]
E = -1

def deflection(M_lst, I_lst, E, ylst):
    num = E * I_lst
    frac = [i / j for i, j in zip(M_lst, num)]
    Defl_lst1 = sp.cumtrapz(frac,ylst,initial=0)
    Defl_lst = sp.cumtrapz(Defl_lst1,ylst,initial=0)

    return Defl_lst

Defl_lst = deflection(M_lst, I_lst, E, ylst0)
print(Defl_lst)

plt.plot(Defl_lst, ylst0, 'rs-', label='Deflection')
plt.axhline(0, color="black")
plt.axvline(0, color="black")
plt.legend()
plt.grid()
plt.show()

