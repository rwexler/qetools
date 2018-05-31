import sys
import numpy as np

##### settings #####
temp = float(sys.argv[1])

##### get vibrational frequencies #####
evalfile = open('evals.dat', 'r')
eval = []
for line in evalfile:
    eval.append(float(line))
eval = np.asarray(eval[:-6])

beta = 1./(8.6173324e-5*temp) # eV/K
wneV = 8065.54401 # cm^-1/eV

helmholtzArray = np.log( np.exp( (beta*eval) / (2.*wneV) ) - np.exp( (-beta*eval) / (2.*wneV) ) )
print(np.sum(helmholtzArray)/beta)
