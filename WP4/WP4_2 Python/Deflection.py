#Defining the functions for returning the deflection
import imp
WP4_XFLR5_Raw_Data = imp.load_source('WP4_XFLR5_Raw_Data','C:\Users\LEMVo\OneDrive\Documenten\LR\AE2111_Systems_Design_Group_D04\WP4\WP4_1 Python\WP4_XFLR5_Raw_Data.py')
from WP4_XFLR5_Raw_Data import ylst_0
import scipy.integrate as sp
import numpy as np
from matplotlib import pyplot as plt

M_lst = [1,2,3,4,5]
I_lst = [2,4,6,8,10]
E = 1

def deflection(M_lst, I_lst, E, ylst):
    exp = M_lst/(E*I_lst)
    V_lst1 = sp.integrate.quad(exp, 0, ylst)
    V_lst2 = sp.integrate.quad(V_lst2, 0, ylst)
    Defl_lst = V_lst2

    return Defl_lst

deflection(M_lst, I_lst, E, ylst0)

plt.plot(Defl_lst, ylst0, 'rs-', label='Deflection')
plt.axhline(0, color="black")
plt.axvline(0, color="black")
plt.xlabel('\u03B1 [deg]', size = 16)
plt.ylabel('C$_l$', size = 16)
plt.legend()
plt.grid()
plt.show()
    
    
