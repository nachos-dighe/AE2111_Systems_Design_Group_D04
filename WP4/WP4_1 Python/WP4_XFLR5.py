import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import interpolate


aerodynamic_data_AOA_0 = np.genfromtxt('MainWing_a=0.00_v=10.00ms.txt', skip_header=2)
aerodynamic_data_AOA_10 = np.genfromtxt('MainWing_a=10.00_v=10.00ms.txt', dtype = float, skip_header=2)

print(aerodynamic_data_AOA_0)