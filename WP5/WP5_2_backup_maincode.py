#Backup for main code

# Main code

#Wingbox dimension lists
alpha, beta, b, DeltaX, Cr = Length.WingboxDimensions(RCr, TCr, Span, y_lst)

#obtain minimal rho satisfying minimum safety factor of 1
min_rho = MinRho.min_rho(c, k1c, M_lst, alpha, beta, b, DeltaX, Cr, t)
print(min_rho)
min_rho = 0.006 #the min rho most limiting neg/pos case
#min_rho not final bc mom of I is not final

#iterate per data point in spanwise direction
for i in range(0,300):
    CG_X, CG_Z = CG.cg_calculation (alpha, beta, b[i], DeltaX[i])
    Ixx = MOI.Ixx_wingbox (DeltaX[i],beta,alpha,CG_Z,t_side,t,b[i])
    Ixz = MOI.Ixz_wingbox(DeltaX[i],beta,alpha,CG_X,CG_Z,t,t_side,b[i])
    Izz = MOI.Izz_wingbox(DeltaX[i],beta,alpha,CG_X,t,t_side,b[i])
    stress_nom = MOI.normal_stress (Ixx,Ixz,Izz,CG_Z,CG_X,abs(M_lst[i]), DeltaX[i], beta)
    safety_margin = StressCon.safety(c, min_rho, k1c, stress_nom)
    SafeMar_lst1.append(safety_margin)
    safety_margin2 = stress_allow / stress_nom
    SafeMar_lst2.append(safety_margin2)
    
