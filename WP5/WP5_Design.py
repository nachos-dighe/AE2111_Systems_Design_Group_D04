#importing x,y lists from WP4
import os
dirname = os.path.dirname(__file__)
dirname = dirname[:-1]+'4' + '\WP4_1 Python'
os.chdir(dirname)
from WP4_XFLR5_Raw_Data import xlst_0, ylst_0

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
    def rib(self, thickness, n_ribs, spacing): #thickness [mm] #spacing is an array
        pass
    def stringer(self, shape, n_stringer_top, n_stringer_bottom): #shape 
        pass
    
#Design 1 (no stringers)
wingbox_1 =Wingbox(1)

#Design 2 (x1 top stringer)

#Design 3 (x1 top and x1 bottom stringer)
    