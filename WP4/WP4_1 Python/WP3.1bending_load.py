import numpy as np
import scipy as sp
from scipy import integrate

def f(x):
    return np.sqrt( 1 - ( x / 40 ) ** 2 )

print( sp.integrate.quad(f,0,40) )

