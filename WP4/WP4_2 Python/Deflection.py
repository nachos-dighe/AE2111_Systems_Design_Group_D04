#Defining the functions for returning the deflection

import ylst
import scipy.integrate as sp
import numpy as np
from matplotlib import pyplot as plt

def deflection(M_lst, I_lst, ylst):
    num = I_lst 
    frac = [i / j for i, j in zip(M_lst, num)]
    Defl_lst1 = sp.cumtrapz(frac,ylst,initial=0)
    Defl_lst = sp.cumtrapz(Defl_lst1,ylst,initial=0)

    return Defl_lst

