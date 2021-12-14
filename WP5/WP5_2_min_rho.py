import WP5_2_CG_Wingbox as CG
import WP5_2_MOI_trial as MOI
import WP5_2_stressconcentration as StressCon

def min_rho(c, k1c, M_lst, alpha, beta, b, DeltaX, Cr, t):    
    #finding max nominal stress:
    i_max = M_lst.index(max(M_lst))
    
    #obtaining the max bending stress in that cross section
    print(alpha, beta, b[i_max], DeltaX[i_max])
    CG_X, CG_Z = CG.cg_calculation (alpha, beta, b[i_max], DeltaX[i_max])
    Ixx = MOI.Ixx_wingbox (DeltaX[i_max],beta,alpha,CG_Z,t,b[i_max])
    Ixz = MOI.Ixz_wingbox(DeltaX[i_max],beta,alpha,CG_X,CG_Z,t,b[i_max])
    Izz = MOI.Izz_wingbox(DeltaX[i_max],beta,alpha,CG_X,t,b[i_max])
    stress_nom = MOI.normal_stress (Ixx,Ixz,Izz,CG_Z,CG_X,M_lst[i_max], DeltaX[i_max], beta)

    #iterate over rho until safety margin >1 is satisfied
    SafeMar_rho_lst = []    
    rho = 0.001 
    while True:
        safety_margin = StressCon.safety(c, rho, k1c, stress_nom)
        if safety_margin >= 1:
            SafeMar_rho_lst.append(safety_margin)
            break
        rho = rho + 0.001
    return rho
