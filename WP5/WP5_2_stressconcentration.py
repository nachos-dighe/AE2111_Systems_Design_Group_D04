#function calculating the increased stress by crack

#c is given in wp and is 5mm
#rho is a variable of which the influence on the design is to be determined
#stress_nom is crackless stress due to bending
def stress_concentration_factor (c, rho, stress_nom): 
    stress_max = (1 + 2*((c/rho)**0.5))*stress_nom
    return stress_max


#function calculating stress at which crack propagates

#c is 5 mm again
#k1c is material property and is 29 MPa
def propagate_stress (c, k1c):
    prop_stress = k1c/((pi * c)**0.5)
    return prop_stress


#function calculating margin of safety
def safety_margin (prop_stress, stress_max):
    safety = prop_stress/stress_max
    return safety

    
