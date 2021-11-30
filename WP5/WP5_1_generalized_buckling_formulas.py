import numpy as np


# average shear
def shear_ave (V_y , y):
    t = 0.00198 #[m]
    tau_ave = V_y / ( 0.0856 * chords[y] + 0.0542 * chords[y] ) 
    
    

# web buckling
def web_buckling ( k_s, b, ):
    # material props 
    E = 207 * ( 10 ** 9 ) # [N/m^2] 
    nu = 0.33

    #wingbox dimensions 
    k_s = k_s
    t = 0.00198 # [m] 

    #max. shear stress for buckling 
    tau_cr = ( ( np.pi * k_s * E ) / ( 12 * ( 1 - nu ** 2 ) )
               * ( ( t / b ) ** 2 )

    return(tau_cr) 


def skin_buckling ( k_c, b, ) :
    #material props
    E = 207 * ( 10 ** 9 ) #[N/m^2]
    nu = 0.33

    #wingbox dimensions 
    k_c = k_c 
    t = 0.00198 # [m]
    
    #  max normal stress for buckling 
    sigma_cr =  ( ( ( np.pi ** 2 * k_c * E ) / ( 12 * ( 1 - nu ** 2 ) ) ) *
                 ( t / b ) ** 2 )

    return sigma_cr 
