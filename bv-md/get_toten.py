import numpy as np
import os
from glob import glob
import sys

# note: themo printed every 100 steps, dump every 200
# last 1000 structures = last 2000 energies
avg_rng = 2 * 1000 # average over last 1000 values

temp_list = np.sort(glob('*/')) # get names of all directories and sort in ascending order
mean_toten = np.zeros((len(temp_list), ))
for i, dir in enumerate(temp_list) :
    os.chdir(dir)

    # get number of runs
    nruns = 0
    with open('files.log', 'r') as file :
        for line in file :
            if 'Step Temp E_angle' in line :
                nruns += 1
    
    # get total energies
    nstop = 0
    with open('files.log', 'r') as file :
        for line in file :
            if 'Step Temp E_angle' in line :
                nstop += 1
            if nstop == nruns :
                break
        toten = []
        for line in file :
            if 'Loop time' in line :
                break
            else :
                toten.append(float(line.split()[3]))
    toten = np.array(toten)[-avg_rng:]
    mean_toten[i] = np.mean(np.array(toten))
    print temp_list[i], mean_toten[i]

    os.chdir('../')
