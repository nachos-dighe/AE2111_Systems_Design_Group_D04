def safety (c, rho, k1c, stress_nom):
    stress_max = (1 + (2*((c/rho)**0.5))*stress_nom)
    stress_prop = k1c/((pi * c)**0.5)
    safety_margin = stress_prop/stress_max
    return safety_margin
