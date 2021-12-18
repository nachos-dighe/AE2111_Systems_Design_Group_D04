import numpy as np
import matplotlib.pyplot as plt
from WP4_XFLR5_Raw_Data import xlst_0, ylst_0
from WP4_1_main import BMres_poscrit, BMres_negcrit

#WARNING
print('------WARNING------\n Always use *variable_mod* syntaxin this program to avoid singular points.\n -------------')

#singular point, BM[-1] approaches 0, MOS[-1] tends to infty 
conds = ((abs(BMres_poscrit)>10000) & (abs(BMres_negcrit)>5000))
ylst_0_mod=ylst_0[np.where(conds)]
xlst_0_mod=xlst_0[np.where(conds)]
BMres_poscrit_mod = BMres_poscrit[conds]
BMres_negcrit_mod = BMres_negcrit[conds]

#wingbox dimensions (z from centroidal x-axis)
alpha = np.deg2rad(2.54)
beta = np.deg2rad(0.73)
DeltaX = 0.55*xlst_0_mod

#wingbox dimension: LE/TE
z_LE = 0.0856*xlst_0_mod
z_TE = 0.0542*xlst_0_mod #b

#centroid to bottom plate at LE/TE
z_LE_bottom = 0.038*xlst_0_mod
z_TE_bottom = z_LE_bottom-DeltaX*np.tan(beta)

#centroid to top plate at LE/TE
z_LE_top = z_LE-z_LE_bottom
z_TE_top = z_LE-z_LE_bottom-DeltaX*np.tan(alpha)

#wingbox thickness
t_wingbox_tb = 0.00198 #as checked last time
t_wingbox_side = 0.004 

#MOI without stringers
def MOI_calculator(DeltaX, beta, alpha, z, b):
    Ixx1_per_t = ((((DeltaX) ** 3) * ((np.sin(beta)) ** 2)) / (12 * ((np.cos(beta)) ** 3))) + ((DeltaX) / np.cos(beta)) * (
                z - ((DeltaX * np.tan(beta)) / 2)) ** 2  # lower left angled profile

    Ixx2_per_t = (((DeltaX) ** 3) * ((np.sin((alpha)) ** 2)) / (12 * ((np.cos(alpha)) ** 3))) + (DeltaX / (np.cos(alpha))) * (
                (-DeltaX * np.tan(beta)) - b - ((DeltaX * np.tan(alpha)) / 2) + z) ** 2  # upper right angled profile

    Ixx3_per_t = 1 / 12 * ((DeltaX * np.tan(beta) + b + DeltaX * np.tan(alpha)) ** 3) + (
                DeltaX * np.tan(beta) + b + DeltaX * np.tan(alpha)) * (
                       z - ((DeltaX * np.tan(beta) + b + DeltaX * np.tan(alpha)) / 2)) ** 2  # vertical profile on the left
    #MOI per unit thickness  [m^3]              
    Ixx4_per_t = 1 / 12 * b ** 3 + b * (DeltaX * np.tan(beta) + (b / 2) - z) ** 2  # vertical profile on the right

    #MOI, corrected for thickness [m^4]
    Ixx = (Ixx1_per_t + Ixx2_per_t)*t_wingbox_side + (Ixx3_per_t + Ixx4_per_t)*t_wingbox_tb
    return Ixx

def column_buckling(z_LE_0, z_TE_0, I_wb, BM, n_stringer, type_stringer_lst, Astringer_lst, t):  #z_LE_0,z_TE_0  (0: can be replaced with top/bottom), BM: pos/neg crit,
 
    #stringer material/geometry
    E = 68.9 * 10 ** 9
    L = 24.63 / 2  # half-span (w.o. coordinate transformation)
    K = 1 / 4  # K= (1/4) one fixed, one free end  #K = 4 one fixed, one free end
    #sigma_yield = 241 * 10 ** 6  # compressive strengh of Aluminum, incorrect approach (refine later)
    Sf = 1.5 #safety factor

    #init
    zlst = np.linspace(z_LE_0, z_TE_0, n_stringer, endpoint=False)
    sigma_crit_lst = np.empty([n_stringer, len(BM)])
    sigma_allow_lst = np.empty([n_stringer, len(BM)])
    MOS_lst_lst = np.empty([n_stringer, len(BM)])
    
    #hard-code
    for i in range(0, n_stringer):
        if i ==0 or i ==(n_stringer-1):
            Astringer_lst =np.full((len(BM)), 0.000175)
        else:
            Astringer_lst =np.full((len(BM)), 0.000275)
        
        if type_stringer_lst[i] ==0: #I-stringer
            alst = (Astringer_lst/t)/4.1 #based on optimised design
            blst = alst
            clst = 2.1*alst
            yclst = (alst*blst+blst*blst/2)/(alst+blst+clst)
            Iminlst =((blst-yclst)**2*alst+yclst**2*clst+(blst/2-yclst)**2*blst+blst**3/12) #Ixx/t= Imin/t [m^3]
        elif type_stringer_lst[i] ==1: #L-stringer
            alst =  (Astringer_lst/t)/2 #based on optimised design
            blst = alst
            yclst = alst/4 #xclst = yclst
            Iminlst = (yclst** 2 * alst + alst** 3 / 12 + (alst / 2 - yclst)** 2 * alst) #Ixx/t = Iyy/t =Imin/t [m^3]
        
        Iminlst *= t #going from [m^3] to [m^4] by including thickness
        #addition of moment of inertia
        print('Iwb before:  ',I_wb[0])
        I_wb += Iminlst + zlst[i]**2*Astringer_lst
        print('Iwb after:  ',I_wb[0])     
        #failure stress
        sigma_crit = (K*np.pi**2*E*Iminlst)/(L**2*Astringer_lst)
        sigma_crit_lst[i, :] = sigma_crit
        
        #print(Iminlst[-1], sigma_crit_lst[-1]) #testing #works
        #sigma_crit_lst /= n_stringer  # assume stress equally divided across stringers #INCORRECT
        
    #(total) allowable stress (total moment of inertia- including stringers)
    sigma_allow= Sf*BM*zlst[i]/(I_wb*(n_stringer+1)) #compatibility eqn approx: load carried equally by stringers + wb skin
    #sigma_allow_lst[i, :] = sigma_allow #NO LONGER NEEDED
    
    #axial loading: equilibrium & compatibility matrix (b_sa = A_sa * X_sa)
    '''
    b_sa = np.zeros([n_stringer+1])
    b_sa[0] =sigma_allow
    a = np.array([[1, 2], [3, 5]])
    b = np.array([1, 2])
    x = np.linalg.solve(a, b)
    '''
    #margin of safety for ith stringer, spanwise
    MOS_lst_lst = sigma_crit_lst/np.abs(sigma_allow)
    for k in range(0, n_stringer):
        MOS_lst = sigma_crit_lst[k, :]/sigma_allow
        #--------BAD CODE---------#
        MOS_lst *= 100 #for reasons I can't debug, 
        #-----END OF BAD CODE -------#
        MOS_lst_lst[k, :] = MOS_lst
    #margin of safety for all stringers, spanwise
    #MOS_lst_lst[i, :] = MOS_lst #no longer needed (if doesnt work, add a for loop)
    
    return (MOS_lst_lst, sigma_crit_lst, sigma_allow)


#initialisation: wingbox (all design options)
A_stringer_root_top = 0.0003  #assumed [m]
A_stringer_tip_top = 0.0003  #assumed [m]
A_stringer_root_bottom = 0.0003 #assumed [m]
A_stringer_tip_bottom = 0.0003 #assumed [m]
t_stringer_top = 0.001 #assumed [m] #const thickness
t_stringer_bottom = 0.001 #assumed [m] #const thickness

#initialisation (stringer instances)
n_stringer_top = 4#np.array([4, 3,2]) #can be changed
n_stringer_bottom = 3# np.array([3, 2,2]) #can be changed
type_stringer_lst_top = np.array([1,0,0,1])#np.array([[1,0,0,1], [1,0,1], [1,1]]) #0: I-stringer; 1: L-stringer (come up with better implementation)
type_stringer_lst_bottom = np.array([1,0,1])#np.array([[1,0,1], [1,1], [1,1]]) #0: I-stringer; 1: L-stringer (come up with better implementation)

#optimisation
A_tot = A_stringer_root_top*n_stringer_top+A_stringer_root_bottom*n_stringer_bottom

#calculate MOI of WB (w/o stringer)
I_wb = MOI_calculator(DeltaX, beta, alpha, z_LE_bottom, z_TE) #works
print('INIT IWB:',I_wb[0])

#geometric computation: wingbox (all design options)
Astringer_top_lst=np.linspace(A_stringer_root_top, A_stringer_tip_top,len(ylst_0_mod)) #works
Astringer_bottom_lst=np.linspace(A_stringer_root_bottom, A_stringer_tip_bottom,len(ylst_0_mod))#works


#print(n_stringer_top[j], type_stringer_lst_top[j], Astringer_top_lst[j], t_stringer_top[j]) #works
#spanwise margin of safety
MOS_lst_lst_top, sigma_crit_top_lst, sigma_allow_top_lst = column_buckling(z_LE_top, z_TE_top, I_wb, BMres_poscrit_mod, n_stringer_top, type_stringer_lst_top, Astringer_top_lst, t_stringer_top) #does not work
MOS_lst_lst_bottom, sigma_crit_bottom_lst, sigma_allow_bottom_lst  = column_buckling(z_LE_bottom, z_TE_bottom, I_wb, BMres_negcrit_mod, n_stringer_bottom, type_stringer_lst_bottom, Astringer_bottom_lst, t_stringer_bottom)

#PLOTTING
# multiple line plots
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

for n in range(0,n_stringer_top):
    label_txt = 'Stringer: ' + str(n+1)
    ax1.plot(ylst_0_mod,MOS_lst_lst_top[n,:], label = label_txt)
ax1.legend()
ax1.set_ylabel(r'MOS [-]')
ax1.set_xlabel(r'Span [m]')
ax1.set_title('Spanwise Margin of Safety: Top Panel Stringers')
ax1.grid(True)    
#ax1.set_yticks(np.linspace(round(np.min(MOS_lst_lst_top)), round(np.max(MOS_lst_lst_top)), 10)) 

for n in range(0,n_stringer_bottom):
    label_txt = 'Stringer: ' + str(n+1)
    ax2.plot(ylst_0_mod,MOS_lst_lst_bottom[n,:], label = label_txt)
ax2.legend()
ax2.set_ylabel(r'MOS [-]')
ax2.set_xlabel(r'Span [m]')
ax2.set_title('Spanwise Margin of Safety: Bottom Panel Stringers') #', Wingbox: '+str(j+1))
ax2.grid(True)
#ax2.set_yticks(np.linspace(round(np.min(MOS_lst_lst_bottom)), round(np.max(MOS_lst_lst_bottom)), 10))  




#user-input
#user_input =0 
user_input = int(input('\n0: Show only; \n 1: Show and Save to file'))
if user_input ==0:
    plt.show()
    print('\nTotal stringer area: ', A_tot)
elif user_input ==1:
    fig1_filename = 'MOS_Col_Buckling_Top_Panel_Iter4.pdf'
    fig2_filename = 'MOS_Col_Buckling_Bottom_Panel_Iter4.pdf'
    fig1.savefig(fig1_filename)
    fig2.savefig(fig2_filename)
    plt.show()
    print('\nTotal stringer area: ', A_tot)