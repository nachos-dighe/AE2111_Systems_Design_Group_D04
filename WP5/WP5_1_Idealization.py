import numpy as np

# parameters
    t = 0.00198
    alp = 2.54 / 180 * np.pi
    bet = 0.73 / 180 * np.pi

    b12 = 0.55 * np.cos(alp) * xlst
    b23 = 0.0542 * xlst
    b34 = 0.55 * np.cos(bet) * xlst
    b14 = 0.0856 * xlst

#idealization

def ideal (xlst, ylst, A_str, M_x, I_xx, I_zz, I_xz): #A is stringer area
   
    #normal stresses in booms

    s_1 =  (( M_x * I_zz * ( 0.038 - 0.0856 ) * xlst - M_x * I_xz * ( 0.268 * xlst ) ) /
           ( I_xx * I_zz - I_xz ** 2 ) )

    s_2 = (( M_x * I_zz * ( 0.038 - ( 0.0542 + 0.007) ) * xlst - M_x * I_xz * ( ( 0.268 - 0.55 ) * xlst ) ) /
           ( I_xx * I_zz - I_xz ** 2 ) )

    s_3 = (( M_x * I_zz * ( 0.038 - 0.007 ) * xlst - M_x * I_xz * ( ( 0.268 - 0.55 ) * xlst ) ) /
           ( I_xx * I_zz - I_xz ** 2 ) )

    s_4 = (( M_x * I_zz * 0.038 * xlst - M_x * I_xz * 0.268 * xlst ) ) /
           ( I_xx * I_zz - I_xz ** 2 ) )

    # boom areas     ## B = (( tskin * b ) / 6 ) * ( 2 + ( s1 / s2 ) )

    B1 = (( t * b12 ) / 6 ) * ( 2 + ( s_2 / s_1 ) ) + (( t * b14 ) / 6 ) * ( 2 + ( s_4 / s_1 ) ) + A_str

    B2 = (( t * b12 ) / 6 ) * ( 2 + ( s_1 / s_2 ) ) + (( t * b23 ) / 6 ) * ( 2 + ( s_3 / s_2 ) ) + A_str

    B3 = (( t * b23 ) / 6 ) * ( 2 + ( s_2 / s_3 ) ) + (( t * b34 ) / 6 ) * ( 2 + ( s_4 / s_3 ) ) + A_str

    B4 = (( t * b34 ) / 6 ) * ( 2 + ( s_3 / s_4 ) ) + (( t * b14 ) / 6 ) * ( 2 + ( s_1 / s_4 ) ) + A_str

    return B1, B2, B3, B4

def shearflow ( xlst, ylst, A_str, M_x, I_xx, I_zz, I_xz, B1, B2, B3, B4, n_t, n_b ):

    ## fix variation of stringers

    #stringer spacing
    spac_t = ( 0.55 * xlst ) / ( n_t + 1 ) # stringer spacing  ALONG CHORD, NOT ALONG SHEET ==>> IT IS THE HORIZONTAL DISTANCE
    spac_b = ( 0.55 * xlst ) / (n_b + 1 )

    # set up table : boom, B, y , y^2 * B , q

##    z_sht = ((0.038 - 0.0856) + 0.55 * np.sin(alp)) x 
##    z_shb = ( 0.038 - 0.55 * np.sin( bet ) ) x

    # for first stringer on top 
    B_r = A_str
    
    def zstr_t (spac, n):
        z_offset_t = ((0.038 - 0.0856) + 0.55 * np.sin(alp)) * spac * n
        return z_offset_t

    def zstr_b (spac, n):
        z_offset_b = ( 0.038 - 0.55 * np.sin( bet ) ) * spac * n
        return z_offset_b

    def dQ (
        

    #I_r = ystr_r ** 2 * B_r

    #top sheet stringers 
    pos_array_t = np.zeros(n_t, len(ylst))
    I_array_t = np.zeros(n_t, len(ylst))
    dQ_array_t = np.zeros(n_t, len(ylst))

    for i in range(n_t): 
        pos_array_t[i,:] = zstr_t( spac_t , i )
        I_array_t[i,:] = pos_array_t[i,:] ** 2 * B_r
        dQ_array 




    











"""
n_t = 6
n_b = 4

alp = 2.54 / 180 * np.pi
bet = 0.73 / 180 * np.pi


ylst = [0,1,2,3,4,5,6,7,8,9,10,11,12]
xlst = [4, 3.75, 3.5, 3.25, 3., 2.75, 2.5, 2.25, 2. , 1.75, 1.5, 1.25, 1 ] 

spac_t = ( 0.55 * np.array(xlst) ) / ( n_t + 1 )  # stringer spacing  ALONG CHORD, NOT ALONG SHEET ==>> IT IS THE HORIZONTAL DISTANCE
spac_b = ( 0.55 * np.array(xlst) ) / (n_b + 1 )

print(spac_t)
print()
print()

##z_sht = ((0.038 - 0.0856) + 0.55 * np.sin(alp)) x 
##z_shb = ( 0.038 - 0.55 * np.sin( bet ) ) x

s_loct = []
x = spac_t 
for i in range(n_t - 1): 
    s_loct.append(x)
    x = x + spac_t

print(s_loct)
    
"""




        



    

    
    


    

    


    

    
