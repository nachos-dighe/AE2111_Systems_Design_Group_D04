import numpy as np
def column_buckling(n_stringer):
    E = 68.9 * 10 ** 9
    L = 24.63 /2 #half-span (w.o. coordinate transformation)
    K = 1/4 #K= (1/4) one fixed, one free end  #K = 4 one fixed, one free end
    sigma_cr = 276*10**6 #compressive strengh of Aluminum, incorrect approach (refine later)
    c_xx = 5/24 #I_xx = c_w_stringer**3*t #dependent on shape
    c_yy = 5/24 #I_yy = w_stringer**3*t #dependent on shape
    c = min(c_xx, c_yy)
    sigma_cr /= n_stringer
    w_stringer = np.sqrt((2*sigma_cr*L**2)/(c*K*np.pi**2*E))
    return(w_stringer)

w_stringer = column_buckling(3)
print(w_stringer) #testing