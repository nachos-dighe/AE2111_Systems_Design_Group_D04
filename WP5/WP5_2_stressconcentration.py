#function calculating the increased stress by crack

#c is given in wp and is 5mm
#rho is a variable of which the influence on the design is to be determined
#k1c fracture toughness which is a material property
#stress_nom is crackless stress due to bending

def safety (c, rho, k1c, stress_nom): 
    stress_max = (1 + 2*((c/rho)**0.5))*stress_nom
    fail_stress = k1c/((pi * c)**0.5)
    safety_margin = fail_stress/stress_max
    return safety_margin
