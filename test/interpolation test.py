'''
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
x = np.arange(0, 10)
y = np.exp(-x/3.0)
f = interpolate.interp1d(x, y)
xnew = np.arange(0, 9, 0.1)
ynew = f(xnew)   # use interpolation function returned by `interp1d`
plt.plot(x, y, 'o', xnew, ynew, '-')
plt.show()
'''


def f(a):
    b = a**2
    e = b+a
    return(b,e)

def g(c,i):
    d = c*2
    j = c-9*i
    return(d,k)

x = 5
print(f(x), type(f(x)))
y= g(list(f(x)).split)
print(y)
    
