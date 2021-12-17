import WP5_2_CG_Wingbox as CG
import WP5_2_MOI as MOI 
import WP5_2_stressconcentration as StressCon

def min_rho(c, k1c, M_lst, alpha, beta, b, DeltaX, Cr, t, DesignChoice,t_side,L_L,t_L,I_c,I_a,I_b,t_I,A_L):    
    #finding max nominal stress:
    i_max = M_lst.index(max(M_lst))    
    #obtaining the max bending stress in that cross section)
    CG_X, CG_Z = CG.cg_calculation (alpha, beta, b[i_max], DeltaX[i_max])
    if "1" in DesignChoice:
        number_of_I_stringers_top = 0
        number_of_I_stringers_bottom = 0
    if "2" in DesignChoice:
        number_of_I_stringers_top = 1
        number_of_I_stringers_bottom = 0
    if "3" in DesignChoice:
        number_of_I_stringers_top = 1
        number_of_I_stringers_bottom = 1
    
    maxstress1, maxstress2, maxstress3 = MOI.normal_stress_calculator(CG_X,CG_Z,alpha,beta,DeltaX[i_max],b[i_max],t_side, t,L_L,t_L,I_c,I_a,I_b,t_I,A_L,abs(M_lst[i_max]))
    if "1" in DesignChoice:
        stress_nom = maxstress1
    if "2" in DesignChoice:
        stress_nom = maxstress2
    if "3" in DesignChoice:
        stress_nom = maxstress3
        
    #iterate over rho until safety margin >1 is satisfied  
    rho = 0.001 
    while True:
        safety_margin = StressCon.safety(c, rho, k1c, stress_nom)
        if safety_margin >= 1 :
            break
        rho = rho + 0.001
    return rho
