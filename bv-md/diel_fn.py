import sys
import os
import numpy as np

temps = np.arange(10, 180, 10)
temp_list = []
for temp in temps :
    if temp < 100 :
        temp_list.append('0' + str(temp) + 'K')
    else :
        temp_list.append(str(temp) + 'K')
betas = 1. / (1.38064852e-23 * temps)

# get dipole moment info
def get_dm_info() :
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
    return mag

# get volume info
def get_vol_info() :
    filename = 'files.lat'
    nsteps = 0
    with open(filename, 'r') as f :
        for line in f:
            nsteps += 1
    lat = np.zeros((nsteps, 3))
    with open(filename, 'r') as f :
        for step in range(nsteps) :
            for line in f :
                lat[step, :] = np.asarray(line.split())[[0, 4, 8]].astype('float')
                break
    vol = np.mean(np.prod(lat, 1) * 1e-30)
    return vol

for i, temp_dir in enumerate(temp_list) :
    os.chdir(temp_dir)

    mag = get_dm_info()
    vol = get_vol_info()
    eta = betas[i] * vol * np.var(mag) * 8.854e12
    print temps[i], eta

    os.chdir('../')
