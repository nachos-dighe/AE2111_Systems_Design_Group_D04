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

