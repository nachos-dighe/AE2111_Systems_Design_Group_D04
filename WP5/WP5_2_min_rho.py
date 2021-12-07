import WP5_2_Chord_Length as Length
import WP5_2_stressconcentration as StressCon
import WP5_2_MOI_trial as MOI
import WP5_2_CG_Wingbox as CG


def min_rho(c, k1c, M_lst, alpha, beta, b, DeltaX, Cr, t):
    #iterate per data point in spanwise direction
    rho_lst = []
    SafeMar_rho_lst = []
    rhodiff_lst = []

    #finding max nominal stress:
    i_max = M_lst.index(max(M_lst))
    
    for i in range(0,300):
    #obtaining the max bending stress in the cross section
        CG_X, CG_Z = CG.cg_calculation (alpha, beta, b[i], DeltaX[i])
        Ixx = MOI.Ixx_wingbox (DeltaX[i],beta,alpha,CG_Z,t,b[i])
        Ixz = MOI.Ixz_wingbox(DeltaX[i],beta,alpha,CG_X,CG_Z,t,b[i])
        Izz = MOI.Izz_wingbox(DeltaX[i],beta,alpha,CG_X,t,b[i])
        stress_nom = MOI.normal_stress (Ixx,Ixz,Izz,CG_Z,CG_X,M_lst[i_max], DeltaX[i], beta)
        
        rho = 0.001
        
        while True:
            safety_margin1 = StressCon.safety(c, rho, k1c, stress_nom)
            rho = rho + 0.001
            safety_margin2 = StressCon.safety(c, rho, k1c, stress_nom)
            difference = ((safety_margin2 - safety_margin1)/safety_margin1)*100
            if safety_margin2 >= 1.5:
                #print(safety_margin2,rho)
                SafeMar_rho_lst.append(safety_margin2)
                rho_lst.append(rho)
                rhodiff_lst.append(difference)
                break
    min_rho = min(rho_lst)
    return min_rho

