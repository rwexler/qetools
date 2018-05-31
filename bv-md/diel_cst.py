import sys
import os
import numpy as np

temp = float(sys.argv[1])
beta = 1. / (1.38064852e-23 * temp)

# get dipole moment info
filename = 'files.DM'
nsteps = 0
with open(filename, 'r') as f :
    for line in f:
        nsteps += 1
dm = np.zeros((nsteps, 3))
with open(filename, 'r') as f :
    for step in range(nsteps) :
        for line in f :
            dm[step, :] = np.asarray(line.split())[1:4].astype('float')
            break
mag = np.sqrt(np.sum(dm**2, 1))

# get volume info
filename = 'files.lat'
lat = np.zeros((nsteps, 3))
with open(filename, 'r') as f :
    for step in range(nsteps) :
        for line in f :
            lat[step, :] = np.asarray(line.split())[[0, 4, 8]].astype('float')
            break
vol = np.mean(np.prod(lat, 1) * 1e-30)

for step in range(nsteps) :
    dms = []
    if step == 1 :
        continue
    else :
        dms.append(mag[:step + 1])
    dms = np.asarray(dms)
    eta = beta * vol * np.var(dms) * 8.854e12
    print step, eta
