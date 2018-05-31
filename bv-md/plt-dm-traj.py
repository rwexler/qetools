from glob import glob
import numpy as np
import os
import sys
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt

# get directories
dirs = sorted([dir for dir in glob("./*") if 'K' in dir])
print 'directories = ', dirs

# convert directories to temperatures
temps = [int(dir[2:-1]) for dir in dirs]
print 'temperatures = ', temps

# make plot directory
os.system('mkdir -p dm-traj')

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

    plt.plot(dm)
    path = '../dm-traj/' + str(temps[i]) + '.pdf'
    plt.savefig(path)
    plt.close()

    os.chdir('../')
