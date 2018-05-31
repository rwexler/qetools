import numpy as np
import os
import sys

#temps = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
#         110, 112, 114, 116, 118,
#         120, 122, 124, 126, 128,
#         130, 132, 134, 136, 138,
#         140, 142, 144, 146, 148,
#         150, 152, 154, 156, 158,
#         160, 165, 170, 175, 180, 185, 190, 195, 200]
temps = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
         110, 120, 130, 140, 150, 160, 170]
temp_list = []
for temp in temps :
    if temp < 100 :
        temp_list.append('0' + str(temp) + 'K')
    else :
        temp_list.append(str(temp) + 'K')

mean_dm = np.zeros((len(temp_list), 3))
for i, dir in enumerate(temp_list) :
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

    mean_dm[i, :] = np.array([np.max(dm[:, 0]) - np.min(dm[:, 0]),
                              np.max(dm[:, 1]) - np.min(dm[:, 1]),
                              np.max(dm[:, 2]) - np.min(dm[:, 2])])

    os.chdir('../')

for i in range(len(temps)) :
    print temps[i], mean_dm[i, 0], mean_dm[i, 1], mean_dm[i, 2]
