import numpy as np

#import ylst, xlst and Vlst, Tlst 

# average shear  #or make spanwise list for all the tau_max? 

def shearweb_tot (ylst, Vlst, xlst, Tlst): # total shear in the webs 
    Cfrac_fr = 0.0865
    Cfrac_re = 0.0542
    Cfrac_le = 0.55
    k_v = #choose reasonable factor 
    t = 0.00198 #[m]

    #shear stress due to shear force 
    taulst_ave = Vlst / ( Cfrac_fr * xlst * t + Cfrac_re * xlst * t )
    taulst_max = tau_ave * k_v

    #shear stress due to torsion
    A_m = ( (Cfrac_fr + Cfrac_re) * Cfrac_le * xlst ) / 2
    q_T = ( Tlst / ( 2 * A_m )
    taulst_T = q_T / t
            
    # total shear in webs 
    tau_tot = tau_maxlst + taulst_T # !!!! differnece between front and rear spar, not okay yet !!!!
            
    return tau_tot

    
# web buckling
def web_buckling ( k_s, y ):
    # material props 
    E = 68.9 * ( 10 ** 9 ) # [N/m^2] 
    nu = 0.33

    #wingbox dimensions 
    k_s = k_s
    t = 0.00198 # [m]
    b_fr = 0.0865 * chord[y]
    b_re = 0.0542 * chord[y] 

    #max. shear stress for buckling 
    tau_cr_fr = ( ( np.pi * k_s * E ) / ( 12 * ( 1 - nu ** 2 ) )
               * ( ( t / b_fr ) ** 2 )

    tau_cr_re = ( ( np.pi * k_s * E ) / ( 12 * ( 1 - nu ** 2 ) )
               * ( ( t / b_re ) ** 2 )

    return(tau_cr_fr, tau_cr_re) 


# --->>> tau_tot should be smaller than t_cr , then no buckling 

""""----------------------------------------------------------------"""' 
def skin_buckling ( k_c, b, ) :
    #material props
    E = 68.9 * ( 10 ** 9 ) #[N/m^2]
    nu = 0.33

    #wingbox dimensions 
    k_c = k_c 
    t = 0.00198 # [m]
    
    #  max normal stress for buckling 
    sigma_cr =  ( ( ( np.pi ** 2 * k_c * E ) / ( 12 * ( 1 - nu ** 2 ) ) ) *
                 ( t / b ) ** 2 )

    return sigma_cr 
