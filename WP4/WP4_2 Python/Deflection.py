#Defining the functions for returning the deflection
from WP4_XFLR5_Raw_Data import ylst_0
import scipy.integrate as sp

M_lst = [1,2,3,4,5]
I_lst = [2,4,6,8,10]
E = 1

def deflection(M_lst, I_lst, E, ylst):
    exp = M_lst/(E*I_lst)
    V_lst1 = sp.integrate.dblquad(
    
    
    
