# importing tools

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate
from scipy import integrate

def y (x) :
    return x ** 3 

print(sp.integrate.quad(y,0,12))











