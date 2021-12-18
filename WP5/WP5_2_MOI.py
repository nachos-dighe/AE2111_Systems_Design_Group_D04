
from math import tan
from math import sin
from math import cos
from math import pi
import math

#1. Ixx Ixz Izz formula for wingbox (Done)
#2. Ixx Ixz Izz local of stringers chosen (Done)
#3. Design type specific total Ixx Ixz Izz (step 1 + design specific stringer configuration) (PARTIALLY DONE)
#4. Stress calculator at extreme points for tension for each design (Done)

############################################################################################################################################################################################


#INPUTS

#dimensions of wingbox: DeltaX,beta,alpha,CG_X, CG_Z,t, t_side


#dimensions of stringers (I & L stringers): L_L, t_L, I_c, I_a, I_b,t_I


#configuration of stringers: number_of_I_stringers_top, number_of_I_stringers_bottom

#extenal loads: M_x at a given point


############################################################################################################################################################################################


#SIDENOTES

#coordinate system: positive z down, positive x right

#alpha and beta should be in radians

#code works by getting a - value for CG_Z (from the output of cg calculator) since it is above datum which is the negative axis


###########################################################################################################################################################################################


#SOME DIMENSIONS

t_side = 4 * 10**(-3) #meters

t = 1.98 * 10**(-3) #meters (for top and bottom sheets)


############################################################################################################################################################################################

#section for wingbox MOI calculation

def normal_stress_calculator(CG_X,CG_Z,alpha,beta,DeltaX,b,t_side, t,L_L,t_L,I_c,I_a,I_b,t_I,A_L,M_x):
    
    def Ixx_wingbox(DeltaX,beta,alpha,CG_Z,t_side,t, b):
    
        Ixx1  =((t*((DeltaX)**3)*((sin(beta))**2))/(12*((cos(beta))**3)))+((t*DeltaX)/cos(beta))*(CG_Z+((DeltaX * tan(beta))/2))**2 #lower left angled profile
    
        Ixx2 = (t*((DeltaX)**3)*((sin((alpha))**2))/(12*((cos(alpha))**3)))+(t*DeltaX/(cos(alpha)))*((DeltaX*tan(beta))+b+((DeltaX*tan(alpha))/2)+CG_Z)**2 #upper right angled profile

        Ixx3 = (1/12) * t_side*((DeltaX*tan(beta)+b+DeltaX*tan(alpha))**3) +t_side*(DeltaX*tan(beta)+b+DeltaX*tan(alpha))*(CG_Z+((DeltaX*tan(beta)+b+DeltaX*tan(alpha))/2))**2 #vertical profile on the left

        Ixx4 = (1/12) * t_side * b**3 + b*t_side*(DeltaX*tan(beta)+(b/2)+CG_Z)**2 #vertical profile on the right

        Ixx_wingbox = Ixx1 + Ixx2 + Ixx3 + Ixx4

        return  Ixx_wingbox

    Ixx_wingbox = Ixx_wingbox(DeltaX,beta,alpha,CG_Z,t,t_side,b)



    def Izz_wingbox(DeltaX,beta,alpha,CG_X,t,t_side,b):

        Izz1 = ((t*((DeltaX)**3)*((cos(beta))**2))/(12*((cos(beta))**3)))+(t*(DeltaX)/cos(beta))*(CG_X-(DeltaX/2))**2    #lower left angled profile

        Izz2 = ((t*(DeltaX)**3)*((cos((alpha))**2))/(12*((cos(alpha))**3)))+(t*DeltaX/(cos(alpha)))*(CG_X-(DeltaX/2))**2   #upper right angled profile

        Izz3 = t_side*(DeltaX * tan(beta) + b + DeltaX * tan(alpha))*((CG_X)**2)  #vertical profile on the left

        Izz4 = t_side*b*((DeltaX-CG_X)**2)   #vertical profile on the right

        Izz_wingbox = Izz1 + Izz2 + Izz3 + Izz4

        return Izz_wingbox

    Izz_wingbox = Izz_wingbox(DeltaX,beta,alpha,CG_X,t,t_side,b)



    def Ixz_wingbox(DeltaX,beta,alpha,CG_X,CG_Z,t,t_side,b): 


        Ixz1 = (1/12) * t * (DeltaX/cos(beta))**3 * sin(beta) * cos(beta) + (DeltaX/cos(beta)) * t * ((DeltaX/2)-CG_X) * (-CG_Z-((DeltaX * tan(beta))/2)) #lower left angled profile (+x)*(+z)

        Ixz2 = (1/12) * t * (DeltaX/cos(alpha))**3 * sin(alpha) * cos(alpha) + (DeltaX/cos(alpha))*t*((DeltaX/2)-CG_X)*(-b-DeltaX *tan(beta)-((DeltaX*tan(alpha))/2)-CG_Z) #upper right angled profile (+x)*(-z)

        Ixz3 = (DeltaX*tan(beta)+b+DeltaX*tan(alpha))*t_side*(-CG_X) * (-CG_Z - (DeltaX * tan(alpha) + b + DeltaX * tan (beta))/2)  #vertical profile on the left (-x)*(+z)

        Ixz4 = b * t_side * (DeltaX - CG_X) * (-CG_Z -((b+DeltaX * tan(beta))/2))  #vertical profile on the right (+x)*(+z)

        Ixz_wingbox = Ixz1 + Ixz2 + Ixz3 + Ixz4

        return Ixz_wingbox

    Ixz_wingbox = Ixz_wingbox(DeltaX,beta,alpha,CG_X,CG_Z,t_side,t,b)
        
    
############################################################################################################################################################################################


#section for local stringer MOI calculation

    def local_MOI_L_stringer_local(L_L,t_L):

        CG_X_L = L_L/4 #right of L stringer

        CG_Z_L = - L_L/4 #above corner of L stringer

        Ixx_L = L_L * t_L * (CG_Z_L)**2 + (1/12) * t_L * (L_L**3) + L_L * t_L *((-t_L/2) - CG_Z_L)**2

        Izz_L = (1/12) * (L_L**3) * t_L + L_L * t_L * ((L_L/2)-CG_X_L)**2 + L_L * t_L * (CG_X_L)**2

        Ixz_L = L_L * t_L * (-CG_X_L) * (-L_L/2 - CG_Z_L) + t_L * L_L * (L_L/2 - CG_X_L) * (-CG_Z_L)

        A_L = 2 * L_L * t_L

        return Ixx_L, Izz_L, Ixz_L, A_L

    Ixx_L,Izz_L, Ixz_L, A_L = local_MOI_L_stringer_local(L_L,t_L)
    

    def local_MOI_I_stringer(I_c, I_a, I_b,t_I):

        CG_Z_I =(I_a * I_b * t_I + 0.5 * I_b * I_b * t_I) /(I_c*t_I + I_b*t_I + I_a*t_I)

        Ixx_I = I_c * t_I * (CG_Z_I)**2 + (1/12) * t_I * (I_b)**3 + t_I * I_b * (0.5 * b - CG_Z_I)**2 + I_a * t_I *(b - CG_Z_I)**2

        Izz_I = (1/12) * (I_a)**3 * t_I + (1/12) *(I_c)**3 * t_I

        Ixz_I = 0 #due to symmetry

        A_I = I_a * t_I + I_b * t_I +I_c * t_I

        return Ixx_I, Izz_I, A_I,Ixz_I

    Ixx_I, Izz_I, A_I, Ixz_I = local_MOI_I_stringer(I_c, I_a, I_b,t_I)




############################################################################################################################################################################################


#section for MOI calculation of each design option

    def I_design_option_1(Ixx_wingbox,Izz_wingbox,Ixz_wingbox, Ixx_L, Izz_L, I_c,I_a,I_b,t_I, A_L, CG_Z, CG_X,DeltaX, b ,alpha, beta,Ixz_L): #no I stringers, only L stringers on corners


        Ixx_design_1 = Ixx_wingbox + Ixx_L + A_L * (CG_Z)**2 + Ixx_L + A_L * (-(DeltaX * tan(alpha) + b + DeltaX * tan(beta)) - CG_Z)**2 + Ixx_L + A_L * (-DeltaX * tan(beta) - CG_Z)**2 + Ixx_L + A_L * (-(DeltaX * tan(alpha) + b)-CG_Z)**2

        Izz_design_1 = Izz_wingbox + 2*(Izz_L + A_L * (CG_X)**2) + 2* (Izz_L + A_L * (DeltaX - CG_X)**2)

        Ixz_design_1 = Ixz_wingbox + 4 * Ixz_L + A_L * (-CG_X)*(-CG_Z) + A_L * (-CG_X) * (-(DeltaX * tan(alpha) + b + DeltaX * tan(beta))-CG_Z) + A_L * (DeltaX - CG_X) * (-CG_Z - DeltaX* tan(beta)) + A_L * (DeltaX - CG_X) * (-(DeltaX * tan(alpha) + b + DeltaX * tan(beta))-CG_Z)

        return Ixx_design_1, Izz_design_1, Ixz_design_1

    Ixx_design_1, Izz_design_1, Ixz_design_1 = I_design_option_1(Ixx_wingbox,Izz_wingbox,Ixz_wingbox, Ixx_L, Izz_L, I_c,I_a,I_b,t_I, A_L, CG_Z, CG_X,DeltaX, b ,alpha, beta,Ixz_L)


    


#assumption: stringers do not have an angle alpha or beta but they are horizontal and the displacement term for the steiners term is from cg of wingbox to vertical position of the sheet and not stringers (stringers relatively small)
    def I_design_option_2(Ixx_design_1,Izz_design_1,Ixz_design_1,CG_Z,DeltaX,alpha,beta,Ixx_I,Izz_I,CG_X,A_I): #one stringer on top


        Ixx_design_2 = Ixx_design_1 + Ixx_I + A_I* (DeltaX*tan(beta)+b+((DeltaX*tan(alpha))/2)+CG_Z)**2

        Izz_design_2 = Izz_design_1 + Izz_I +A_I* ((DeltaX/2)-CG_X)**2

        Ixz_design_2 = Ixz_design_1 + A_I*(-DeltaX*tan(beta)-b-((DeltaX*tan(alpha))/2)-CG_Z) * ((DeltaX/2)-CG_X)

        return Ixx_design_2,Izz_design_2,Ixz_design_2
    
    Ixx_design_2, Izz_design_2, Ixz_design_2 = I_design_option_2(Ixx_design_1,Izz_design_1,Ixz_design_1,CG_Z,DeltaX,alpha,beta,Ixx_I,Izz_I,CG_X,A_I)


    def I_design_option_3(Ixx_design_1,Ixz_design_1,Izz_design_1,CG_X,CG_Z,DeltaX,alpha,beta,b,Ixx_I,Izz_I,A_I): #one stringer on top and one on bottom

        
        Ixx_design_3 = Ixx_design_1 + 3 * Ixx_I + A_I * ((DeltaX * tan(beta) + b + ((2 * DeltaX * tan(alpha))/3))+CG_Z)**2 + A_I * (DeltaX * tan(beta) + b + ((DeltaX * tan(alpha))/3)+CG_Z)**2 + A_I * (((DeltaX * tan(beta))/2)+CG_Z)**2

        Izz_design_3 = Izz_design_1 + 3 * Izz_I + A_I *(CG_X -(DeltaX/3))**2 + A_I *(((2*DeltaX)/3)-CG_X)**2 + A_I *((DeltaX/2)-CG_X)**2

        Ixz_design_3 = Ixz_design_1 + 3 * Ixz_I + A_I * ((DeltaX/3) - CG_X)*(-DeltaX*tan(beta) - b - ((2/3) * DeltaX * tan(alpha))-CG_Z) + A_I * (((2*DeltaX)/3)-CG_X)*(-DeltaX *tan(beta)-b-((1/3)*DeltaX * tan(alpha))-CG_Z) + A_I * (((DeltaX/2)-CG_X)*(-(1/2)*DeltaX * tan(beta))-CG_Z)
        

        return Ixx_design_3,Izz_design_3,Ixz_design_3

    Ixx_design_3,Izz_design_3,Ixz_design_3 = I_design_option_3(Ixx_design_2,Ixz_design_2,Izz_design_2,CG_X,CG_Z,DeltaX,alpha,beta,b,Ixx_I,Izz_I,A_I)


    



############################################################################################################################################################################################

#section for normal stress calculation for each design option
    
    def maximum_tensile_stress(M_x, Izz_design_1,CG_Z,Ixz_design_1,CG_X, Ixx_design_1,DeltaX,beta,Izz_design_2,Ixz_design_2,Ixx_design_2,Izz_design_3,Ixz_design_3,Ixx_design_3):
        max_tensile_Stress_1_design_1 = abs((M_x * Izz_design_1* (-CG_Z) + M_x * Ixz_design_1 * (-CG_X))/(Ixx_design_1*Izz_design_1-((Ixz_design_1)**2)))
        max_tensile_Stress_2_design_1 = abs((M_x * Izz_design_1 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_1 * (DeltaX-CG_X))/(Ixx_design_1*Izz_design_1-((Ixz_design_1)**2)))
        max_stress_design_1 = max(max_tensile_Stress_1_design_1,max_tensile_Stress_2_design_1)
    

        max_tensile_Stress_1_design_2 = abs((M_x * Izz_design_2 * (-CG_Z) + M_x * Ixz_design_2 * (-CG_X))/(Ixx_design_2*Izz_design_2-((Ixz_design_2)**2)))
        max_tensile_Stress_2_design_2 = abs((M_x * Izz_design_2 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_2 * (DeltaX-CG_X))/(Ixx_design_2*Izz_design_2-((Ixz_design_2)**2)))
        max_stress_design_2 = max(max_tensile_Stress_1_design_2,max_tensile_Stress_2_design_2)

        max_tensile_Stress_1_design_3 = (M_x * Izz_design_3 * (-CG_Z) + M_x * Ixz_design_3 * (-CG_X))/(Ixx_design_3*Izz_design_3-((Ixz_design_3)**2))
        max_tensile_Stress_2_design_3 = (M_x * Izz_design_3 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_3 * (DeltaX-CG_X))/(Ixx_design_3*Izz_design_3-((Ixz_design_3)**2))
        max_stress_design_3 = max(max_tensile_Stress_1_design_3,max_tensile_Stress_2_design_3)

        return max_stress_design_1,max_stress_design_2,max_stress_design_3

    max_stress_design_1,max_stress_design_2,max_stress_design_3 = maximum_tensile_stress(M_x, Izz_design_1,CG_Z,Ixz_design_1,CG_X, Ixx_design_1,DeltaX,beta,Izz_design_2,Ixz_design_2,Ixx_design_2,Izz_design_3,Ixz_design_3,Ixx_design_3)


    return max_stress_design_1,max_stress_design_2,max_stress_design_3





