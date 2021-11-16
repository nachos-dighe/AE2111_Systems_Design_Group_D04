# importing tools

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import sympy as sym

#define x as a symbol 
x = sym.Symbol('x')

# define function
def f1(x) :
    return x

def f2 (x) :
    return 2 * x ** 3

<<<<<<< HEAD
# shear calculator 
def shear(f, x):
    S = sym.integrate(f,x) * (-1)
    return S
=======
def d (x):
    return 2 * x - 1 
>>>>>>> 9ffd309e4bf6484aebb75e502dca7dbd7e4ab40b

# shear calculator 
def shear(f, x):
    S = sym.integrate(f,x) * (-1)
    return S

# bending calculator 
def bending(f,x) :
    S = sym.integrate(f,x)
    B = sym.integrate(S,x)
    return B

# bending calculator 
def bending(f,x) :
    S = sym.integrate(f,x)
    B = sym.integrate(S,x)
    return B

#torsion calculator
def torsion(f,x):
    

print(shear( f1(x) , x ) )
print(bending( f1(x) , x ) )

sfunction = shear( f1(x) , x )
bfunction = bending( f1(x) , x )

sym.plot(sfunction,(x,0,12.32))
sym.plot(bfunction,(x,0,12.32))


 

#torsion calculator
def torsion(f,x, d):
    t = f * d
    T = sym.integrate(t,x)
    return T
    
    
print(shear( f1(x) , x ) )
print(bending( f1(x) , x ) )


    
sfunction = shear( f1(x) , x )
bfunction = bending( f1(x) , x )
tfunction = torsion(f1(x) , x , d(x) )
    
sym.plot(sfunction,(x,0,12.32))
sym.plot(bfunction,(x,0,12.32))
sym.plot(tfunction, (x,0,12.32))
            
    

 





