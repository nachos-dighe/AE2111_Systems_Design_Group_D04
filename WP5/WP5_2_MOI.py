
from math import tan
from math import sin
from math import cos
from math import pi
import math

#1. Ixx Ixz Izz formula for wingbox (Done)
#2. Ixx Ixz Izz local of stringers chosen (Done)
#3. Design type specific total Ixx Ixz Izz (step 1 + design specific stringer configuration) (Waiting)
#4. Stress calculator at extreme points for tension for each design (Done)

############################################################################################################################################################################################


#INPUTS

#dimensions of wingbox: DeltaX,beta,alpha,CG_X, CG_Z,t


#dimensions of stringers (I & L stringers): L_L, t_L, I_c, I_a, I_b,t_I


#configuration of stringers: number_of_I_stringers_top, number_of_I_stringers_bottom,  number_of_I_stringers_top, number_of_I_stringers_bottom

#extenal loads: M_x 


############################################################################################################################################################################################


#SIDENOTES

#coordinate system: positive z down, positive x right

#alpha and beta should be in radians

#code works by getting a - value for CG_Z (from the output of cg calculator) since it is above datum which is the negative axis


###########################################################################################################################################################################################


#SOME DIMENSIONS

t = 4 * 10**(-3) #meters


############################################################################################################################################################################################

#section for wingbox MOI calculation


def Ixx_wingbox(DeltaX,beta,alpha,CG_Z,t, b):
    
    Ixx1  =((t*((DeltaX)**3)*((sin(beta))**2))/(12*((cos(beta))**3)))+((t*DeltaX)/cos(beta))*(CG_Z+((DeltaX * tan(beta))/2))**2 #lower left angled profile
    
    Ixx2 = (t*((DeltaX)**3)*((sin((alpha))**2))/(12*((cos(alpha))**3)))+(t*DeltaX/(cos(alpha)))*((DeltaX*tan(beta))+b+((DeltaX*tan(alpha))/2)+CG_Z)**2 #upper right angled profile

    Ixx3 = (1/12) * t*((DeltaX*tan(beta)+b+DeltaX*tan(alpha))**3) +t*(DeltaX*tan(beta)+b+DeltaX*tan(alpha))*(CG_Z+((DeltaX*tan(beta)+b+DeltaX*tan(alpha))/2))**2 #vertical profile on the left

    Ixx4 = (1/12) * t * b**3 + b*t*(DeltaX*tan(beta)+(b/2)+CG_Z)**2 #vertical profile on the right

    Ixx_wingbox = Ixx1 + Ixx2 + Ixx3 + Ixx4

    return  Ixx_wingbox

Ixx_wingbox = Ixx_wingbox(DeltaX,beta,alpha,CG_Z,t,b)



def Izz_wingbox(DeltaX,beta,alpha,CG_X,t,b):

    Izz1 = ((t*((DeltaX)**3)*((cos(beta))**2))/(12*((cos(beta))**3)))+(t*(DeltaX)/cos(beta))*(CG_X-(DeltaX/2))**2    #lower left angled profile

    Izz2 = ((t*(DeltaX)**3)*((cos((alpha))**2))/(12*((cos(alpha))**3)))+(t*DeltaX/(cos(alpha)))*(CG_X-(DeltaX/2))**2   #upper right angled profile

    Izz3 = t*(DeltaX * tan(beta) + b + DeltaX * tan(alpha))*((CG_X)**2)  #vertical profile on the left

    Izz4 = t*b*((DeltaX-CG_X)**2)   #vertical profile on the right

    Izz_wingbox = Izz1 + Izz2 + Izz3 + Izz4

    return Izz_wingbox

Izz_wingbox = Izz_wingbox(DeltaX,beta,alpha,CG_X,t,b)



def Ixz_wingbox(DeltaX,beta,alpha,CG_X,CG_Z,t,b): 


    Ixz1 = (1/12) * t * (DeltaX/cos(beta))**3 * sin(beta) * cos(beta) + (DeltaX/cos(beta)) * t * ((DeltaX/2)-CG_X) * (-CG_Z-((DeltaX * tan(beta))/2)) #lower left angled profile (+x)*(+z)

    Ixz2 = (1/12) * t * (DeltaX/cos(alpha))**3 * sin(alpha) * cos(alpha) + (DeltaX/cos(alpha))*t*((DeltaX/2)-CG_X)*(-b-DeltaX *tan(beta)-((DeltaX*tan(alpha))/2)-CG_Z) #upper right angled profile (+x)*(-z)

    Ixz3 = (DeltaX*tan(beta)+b+DeltaX*tan(alpha))*t*(-CG_X) * (-CG_Z - (DeltaX * tan(alpha) + b + DeltaX * tan (beta))/2)  #vertical profile on the left (-x)*(+z)

    Ixz4 = b * t * (DeltaX - CG_X) * (-CG_Z -((b+DeltaX * tan(beta))/2))  #vertical profile on the right (+x)*(+z)

    Ixz_wingbox = Ixz1 + Ixz2 + Ixz3 + Ixz4

    return Ixz_wingbox

Ixz_wingbox = Ixz_wingbox(DeltaX,beta,alpha,CG_X,CG_Z,t,b)
    
    
############################################################################################################################################################################################


#section for local stringer MOI calculation

def local_MOI_L_stringer_local(L_L,t_L):

    CG_X_L = L_L/4 #right of L stringer

    CG_Z_L = - L_L/4 #above corner of L stringer

    Ixx_L = L_L * t_L * (CG_Z_L)**2 + (1/12) * t_L * (L_L**3) + L_L * t_L *((-L_L/2) - CG_Z_L)**2

    Izz_L = (1/12) * (L_L**3) * t_L + L_L * t_L * ((L_L/2)-CG_X_L)**2 + L_L * t_L * (CG_X_L)**3

    return Ixx_L, Izz_L

Ixx_L,Izz_L = local_MOI_L_stringer_local(L_L,t_L)


def local_MOI_I_stringer(I_c, I_a, I_b,t_I):

    CG_Z_I =(I_a * I_b * t_I + 0.5 * I_b * I_b * t_I) /(I_c*t_I + I_b*t_I + I_a*t_I)

    Ixx_I = I_c * t_I * (CG_Z_I)**2 + (1/12) * t_I * (I_b)**3 + t_I * I_b * (0.5 * b - CG_Z_I)**2 + I_a * t_I *(b - CG_Z_I)**2

    Izz_L = (1/12) * (I_a)**3 * t_I + (1/12) *(I_c)**3 * t_I


    return Ixx_I, Izz_I

Ixx_I, Izz_I = local_MOI_I_stringer(I_c, I_a, I_b,t_I)


def I_stringer_spacing(DeltaX, number_of_I_stringers_top,number_of_I_stringers_bottom):
    #s = spacing between I stringers or between I and L stringers

    s_top = DeltaX / (number_of_I_stringers_top + 1)

    s_bottom = DeltaX / (number_of_I_stringers_bottom + 1)

    return s_top, s_bottom

s_top, s_bottom = I_stringer_spacing(DeltaX, number_of_I_stringers_top,number_of_I_stringers_bottom)






############################################################################################################################################################################################


#section for MOI calculation of each design option

def I_design_option_1(Ixx_wingbox,Izz_wingbox,Ixz_wingbox, Ixx_L, Izz_L, I_c,I_a,I_b,t_I, number_of_I_stringers_top, number_of_I_stringers_bottom, A_L, CG_Z, CG_X,DeltaX, b ,alpha, beta): #no I stringers, only L stringers on corners

    A_L = 300 * (10**-6) #area of single L stringer 

    number_of_I_stringers_top = 0 #number of center stringer on top sheet

    number_of_I_stringers_bottom = 0 #number of center stringer on bottom sheet

    Ixx_design_1 = Ixx_wingbox + Ixx_L + A_L * (CG_Z)**2 + Ixx_L + A_L * (-(DeltaX * tan(alpha) + b + DeltaX * tan(beta)) - CG_Z)**2 + Ixx_L + A_L * (-DeltaX * tan(beta) - CG_Z)**2 + Ixx_L + A_L * (-(DeltaX * tan(alpha) + b)-CG_Z)**2

    Izz_design_1 = Izz_wingbox + 2*(Izz_L + A_L * (CG_X)**2) + 2* (Izz_L + A_L * (DeltaX - CG_X)**2)

    Ixz_design_1 = Ixz_wingbox + A_L * (-CG_X)*(-CG_Z) + A_L * (-CG_X) * (-(DeltaX * tan(alpha) + b + DeltaX * tan(beta))-CG_Z) + A_L * (DeltaX - CG_X) * (-CG_Z - DeltaX* tan(beta)) + A_L * (DeltaX - CG_X) * (-(DeltaX * tan(alpha) + b + DeltaX * tan(beta))-CG_Z)

    return Ixx_design_1, Izz_design_1, Ixz_design_1

Ixx_design_1, Izz_design_1, Ixz_design_1 = I_design_option_1(Ixx_wingbox,Izz_wingbox,Ixz_wingbox, Ixx_L, Izz_L, number_of_I_stringers_top, number_of_I_stringers_bottom, A_L, CG_Z, CG_X,DeltaX, b,alpha, beta)





















############################################################################################################################################################################################

#section for normal stress calculation for each design option
    

def normal_stress_design_1(Ixx_design_1,Ixz_design_1,Izz_design_1,CG_Z,CG_X,M_x):
    sigma_y = (M_x * Izz_design_1 * z + M_x * Ixz_design_1* x)/(Ixx_design_1*Izz_design_1-((Ixz_design_1)**2))

        #we thing that the sign between the two terms in the numerator is + but from normal stress equation is should be -.
        #We think it should be + since we defined x + right, in formula sheet its defined x + left.

        # 2 critical positions for max tension (bottom left or bottom right)

    max_tensile_Stress_1 = (M_x * Izz_design_1* (-CG_Z) + M_x * Ixz_design_1 * (-CG_X))/(Ixx_design_1*Izz_design_1-((Ixz_design_1)**2))

    max_tensile_Stress_2 = (M_x * Izz_design_1 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_1 * (DetlaX-CG_X))/(Ixx_design_1*Izz_design_1-((Ixz_design_1)**2))

    max_tensile_Stress_design_1 = max(max_tensile_Stress_1,max_tensile_Stress_2)

    return max_tensile_stress_design_1

max_tensile_stress_design_1 = normal_stress_design_1(Ixx_design_1,Ixz_design_1,Izz_design_1,CG_Z,CG_X,M_x)
        
def normal_stress_design_2(Ixx_design_2,Ixz_design_2,Izz_design_2,CG_Z,CG_X,M_x):
    sigma_y = (M_x * Izz_design_2 * z + M_x * Ixz_design_2 * x)/(Ixx_design_2*Izz_design_2-((Ixz_design_2)**2))

        #we thing that the sign between the two terms in the numerator is + but from normal stress equation is should be -.
        #We think it should be + since we defined x + right, in formula sheet its defined x + left.

        # 2 critical positions for max tension (bottom left or bottom right)

    max_tensile_Stress_1 = (M_x * Izz_design_2 * (-CG_Z) + M_x * Ixz_design_2 * (-CG_X))/(Ixx_design_2*Izz_design_2-((Ixz_design_2)**2))

    max_tensile_Stress_2 = (M_x * Izz_design_2 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_2 * (DetlaX-CG_X))/(Ixx_design_2*Izz_design_2-((Ixz_design_2)**2))

    max_tensile_Stress_design_2 = max(max_tensile_Stress_1,max_tensile_Stress_2)

    return max_tensile_stress_design_2

max_tensile_stress_design_2 = normal_stress_design_2(Ixx_design_2,Ixz_design_2,Izz_design_2,CG_Z,CG_X,M_x)
        

    
def normal_stress_design_3(Ixx_design_3,Ixz_design_3,Izz_design_3,CG_Z,CG_X,M_x):
    sigma_y = (M_x * Izz_design_3 * z + M_x * Ixz_design_3 * x)/(Ixx_design_3*Izz_design_3-((Ixz_design_3)**2))

        #we thing that the sign between the two terms in the numerator is + but from normal stress equation is should be -.
        #We think it should be + since we defined x + right, in formula sheet its defined x + left.

        # 2 critical positions for max tension (bottom left or bottom right)

    max_tensile_Stress_1 = (M_x * Izz_design_3 * (-CG_Z) + M_x * Ixz_design_3 * (-CG_X))/(Ixx_design_3*Izz_design_3-((Ixz_design_3)**2))

    max_tensile_Stress_2 = (M_x * Izz_design_3 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_3 * (DetlaX-CG_X))/(Ixx_design_3*Izz_design_3-((Ixz_design_3)**2))

    max_tensile_Stress_design_3 = max(max_tensile_Stress_1,max_tensile_Stress_2)

    return max_tensile_stress_design_3

max_tensile_stress_design_3 = normal_stress_design_3(Ixx_design_3,Ixz_design_3,Izz_design_3,CG_Z,CG_X,M_x)
   
    





