from math import *
def safety (c, rho, k1c, stress_nom):
    stress_max = (1 + (2*((c/rho)**0.5))*stress_nom)
    fail_stress = k1c/((pi * c)**0.5)
    safety_margin = fail_stress/stress_max
    return safety_margin
