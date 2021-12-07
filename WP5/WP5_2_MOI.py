
from math import tan
from math import sin
from math import cos
from math import pi
import math

#1. Ixx Ixz Izz formula for wingbox (Done)
#2. Ixx Ixz Izz local of stringers chosen 
#3. Design type specific total Ixx Ixz Izz (step 1 + design specific stringer configuration)
#4. Stress calculator at extreme points for tension for each design





t = 1.98 * 10**(-3)

#inputs: all dimensions of the wingbox including angle and CG location, dimensions of the stringers and their position wrt datum point, moment along the span

#coordinate system: positive z down, positive x right

#VERY IMPORTANT: CG_X VALUE IS +, CG_Z VALUE IS NEGATIVE (from the output of cg calculator)



############################################################################################################################################################################################

#section for wingbox MOI calculation


def Ixx_wingbox(DeltaX,beta,alpha,CG_Z,t):
    
    Ixx1  =((t*((DeltaX)**3)*((sin(beta))**2))/(12*((cos(beta))**3)))+((t*DeltaX)/cos(beta))*(-CG_Z+((DeltaX * tan(beta))/2))**2 #lower left angled profile
    
    Ixx2 = (t*((DeltaX)**3)*((sin((alpha))**2))/(12*((cos(alpha))**3)))+(t*DeltaX/(cos(alpha)))*((-DeltaX*tan(beta))-b-((DeltaX*tan(alpha))/2)+CG_Z)**2 #upper right angled profile

    Ixx3 = (1/12) * t*((DeltaX*tan(beta)+b+DeltaX*tan(alpha))**3) +t*(DeltaX*tan(beta)+b+DeltaX*tan(alpha))*(CG_Z-((DeltaX*tan(beta)+b+DeltaX*tan(alpha))/2))**2 #vertical profile on the left

    Ixx4 = (1/12) * t * b**3 + b*t*(DeltaX*tan(beta)+(b/2)-CG_Z)**2 #vertical profile on the right

    Ixx_wingbox = Ixx1 + Ixx2 + Ixx3 + Ixx4

    return  Ixx_wingbox



def Izz_wingbox(DeltaX,beta,alpha,CG_X,t):

    Izz1 = ((t*((DeltaX)**3)*((cos(beta))**2))/(12*((cos(beta))**3)))+(t*(DeltaX)/cos(beta))*(CG_X-(DeltaX/2))**2    #lower left angled profile

    Izz2 = ((t*(DeltaX)**3)*((cos((alpha))**2))/(12*((cos(alpha))**3)))+(t*DeltaX/(cos(alpha)))*(CG_X-(DeltaX/2))**2   #upper right angled profile

    Izz3 = t*(DeltaX * tan(beta) + b + DeltaX * tan(alpha))*((CG_X)**2)  #vertical profile on the left

    Izz4 = t*b*((DeltaX-CG_X)**2)   #vertical profile on the right

    Izz_wingbox = Izz1 + Izz2 + Izz3 + Izz4

    return Izz_wingbox



def Ixz_wingbox(DeltaX,beta,alpha,CG_X,CG_Z,t): 


    Ixz1 = (1/12) * t * (DeltaX/cos(beta))**3 * sin(beta) * cos(beta) + (DeltaX/cos(beta)) * t * ((DeltaX/2)-CG_X) * (-CG_Z-((DeltaX * tan(beta))/2)) #lower left angled profile (+x)*(+z)

    Ixz2 = (1/12) * t * (DeltaX/cos(alpha))**3 * sin(alpha) * cos(alpha) + (DeltaX/cos(alpha))*t*((DeltaX/2)-CG_X)*(-b-DeltaX *tan(beta)-((DeltaX*tan(alpha))/2)-CG_z) #upper right angled profile (+x)*(-z)

    Ixz3 = (DeltaX*tan(beta)+b+DeltaX*tan(alpha))*t*(-CG_X) * (-CG_Z - (DeltaX * tan(alpha) + b + DeltaX * tan (beta))/2)  #vertical profile on the left (-x)*(+z)

    Ixz4 = b * t * (DeltaX - CG_X) * (-CG_Z -((b+DeltaX * tan(beta))/2))  #vertical profile on the right (+x)*(+z)

    Ixz_wingbox = Ixz1 + Ixz2 + Ixz3 + Ixz4

    return Ixz_wingbox
    
    
############################################################################################################################################################################################


#section for local stringer MOI calculation 








#input stringer dimensions and shape










############################################################################################################################################################################################


#section for MOI calculation of each design option




#input wingbox moi xx zz xz, stringer local moi, number of stringers, stringer positions












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

        
def normal_stress_design_2(Ixx_design_2,Ixz_design_2,Izz_design_2,CG_Z,CG_X,M_x):
    sigma_y = (M_x * Izz_design_2 * z + M_x * Ixz_design_2 * x)/(Ixx_design_2*Izz_design_2-((Ixz_design_2)**2))

        #we thing that the sign between the two terms in the numerator is + but from normal stress equation is should be -.
        #We think it should be + since we defined x + right, in formula sheet its defined x + left.

        # 2 critical positions for max tension (bottom left or bottom right)

    max_tensile_Stress_1 = (M_x * Izz_design_2 * (-CG_Z) + M_x * Ixz_design_2 * (-CG_X))/(Ixx_design_2*Izz_design_2-((Ixz_design_2)**2))

    max_tensile_Stress_2 = (M_x * Izz_design_2 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_2 * (DetlaX-CG_X))/(Ixx_design_2*Izz_design_2-((Ixz_design_2)**2))

    max_tensile_Stress_design_2 = max(max_tensile_Stress_1,max_tensile_Stress_2)

    return max_tensile_stress_design_2
        

    
def normal_stress_design_3(Ixx_design_3,Ixz_design_3,Izz_design_3,CG_Z,CG_X,M_x):
    sigma_y = (M_x * Izz_design_3 * z + M_x * Ixz_design_3 * x)/(Ixx_design_3*Izz_design_3-((Ixz_design_3)**2))

        #we thing that the sign between the two terms in the numerator is + but from normal stress equation is should be -.
        #We think it should be + since we defined x + right, in formula sheet its defined x + left.

        # 2 critical positions for max tension (bottom left or bottom right)

    max_tensile_Stress_1 = (M_x * Izz_design_3 * (-CG_Z) + M_x * Ixz_design_3 * (-CG_X))/(Ixx_design_3*Izz_design_3-((Ixz_design_3)**2))

    max_tensile_Stress_2 = (M_x * Izz_design_3 * (-CG_Z-(DeltaX*tan(beta))) + M_x * Ixz_design_3 * (DetlaX-CG_X))/(Ixx_design_3*Izz_design_3-((Ixz_design_3)**2))

    max_tensile_Stress_design_3 = max(max_tensile_Stress_1,max_tensile_Stress_2)

    return max_tensile_stress_design_3
   
    





