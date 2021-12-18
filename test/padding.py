#matrix test
import numpy as np

n = 3

sigma_allow_tot = 1324
b = np.zeros([n])
b=np.pad(b, (1, 0), 'constant', constant_values=(sigma_allow_tot, 0))

A = np.zeros((n+1, n+1), dtype = float)
np.fill_diagonal(A, -1)
A[0,:] = 1
A[:,0] = 1

#X_sa = np.array([n+1])
X_sa = np.linalg.solve(A, b)

