#importing x,y lists from WP4
import numpy as np
import os
dirname = os.path.dirname(__file__)
dirname = dirname[:-1]+'4' + '\WP4_1 Python'
os.chdir(dirname)
from WP4_XFLR5_Raw_Data import xlst_0, ylst_0

# Wing #(put constants outside class)
Span = 24.63  # [m] Wingpsan
RCr = 4.4  # [m] Root chord
TCr = 1.76  # [m] Tip chord

class Wingbox:
    #cross-section constant
    length =  max(ylst_0)-min(ylst_0)
    alpha  =(2.54121433)*(3.14159265359/180) # rad
    beta = (0.72736298)*(3.14159265359/180)  # rad

    #spanwise lists
    DeltaX = (0.75 - 0.2) * xlst_0
    b = 0.05423628 * xlst_0 #CATIA generated
    FSparL = 0.08562876 * xlst_0 #CATIA generated
    
    def __init__(self, thickness): #thickness [mm]
        pass
    def ribs(self, thickness, n_ribs): #thickness [mm] #spacing is an array in [m]
        rib_spacing = np.full(n_ribs,Span/(2*(n_ribs-1))) #assume uniform spacing (refine later, input as array)
        rib_pos = 0 
        DeltaX_rib = np.empty(n_ribs)
        b_rib = np.empty(n_ribs)
        FSparL_rib = np.empty(n_ribs)        
        for i in range(n_ribs):
            x = RCr - 2*(RCr-TCr)/Span * rib_pos
            #x = np.where(np.min(abs(b/2-ylst_0)), xlst_0)  #does not work
            #x =xlst_0(np.argmin(abs(b/2-ylst_0))) #object not callable error
            
            #modify later, to subtract thickness
            np.append(DeltaX_rib,(0.75 - 0.2) * x)
            np.append(b_rib, 0.05423628 * x) #CATIA generated
            np.append(FSparL_rib, 0.08562876 * x) #CATIA generated
            rib_pos += rib_spacing[i] #change when turned into an array
        return(DeltaX_rib, b_rib, FSparL_rib, rib_pos)
        
    def stringer(self, shape, n_stringer_top, n_stringer_bottom): #shape 
        pass
    
t = 1.98 #const for all wingboxes
#Design 1 (no stringers)
wingbox_1 =Wingbox(t)
DeltaX_rib_1, b_rib_1, FSparL_rib_1, rib_pos_1= wingbox_1.ribs(1, 3) #arbitrary
pass #stringer, stiffeners

#Design 2 (x1 top stringer)
wingbox_2 =Wingbox(t)
DeltaX_rib_2, b_rib_2, FSparL_rib_2, rib_pos_2= wingbox_2.ribs(1, 3) #arbitrary
pass #stringer, stiffeners

#Design 3 (x1 top and x1 bottom stringer)
wingbox_3 =Wingbox(t)
DeltaX_rib_3, b_rib_3, FSparL_rib_3, rib_pos_3= wingbox_3.ribs(1, 3) #arbitrarypass #stringer, stiffenerspass #stringer, stiffeners
pass #stringer, stiffeners
