import numpy as np
import os
import sys
from glob import glob

avg_rng = 1000 # average over last 1000 values

# get directories
dirs = sorted([dir for dir in glob("./*") if 'K' in dir])
print 'directories = ', dirs

# convert directories to temperatures
temps = [int(dir[2:-1]) for dir in dirs]
print 'temperatures = ', temps

# calculate average |polarization|
mean_dm = np.zeros((len(dirs), 3))
for i, dir in enumerate(dirs) :
    os.chdir(dir)

    num_ts = 0
    with open('files.DM', 'r') as f:
        for line in f:
            num_ts += 1

    dm = np.zeros((num_ts, 3))
    with open('files.DM', 'r') as f:
        for row in range(num_ts) :
            for line in f :
                dm[row, :] = np.asarray(line.split())[1:4].astype('float')
                break

    mean_dm[i, :] = np.array([np.mean(dm[-avg_rng:, 0]),
                              np.mean(dm[-avg_rng:, 1]),
                              np.mean(dm[-avg_rng:, 2])])

    os.chdir('../')

for i in range(len(temps)) :
    print temps[i], mean_dm[i, 0], mean_dm[i, 1], mean_dm[i, 2]
