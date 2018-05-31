import numpy as np
import os

temps = np.arange(10, 180, 10)
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
    with open('files.lat', 'r') as f:
        for line in f:
            num_ts += 1

    dm = np.zeros((num_ts, 3))
    with open('files.lat', 'r') as f:
        for row in range(num_ts) :
            for line in f :
                a = float(line.split()[0])
                b = float(line.split()[4])
                c = float(line.split()[8])
                dm[row, :] = np.asarray([a, b, c])
                break

    mean_dm[i, :] = np.array([np.mean(dm[:, 0]),
                              np.mean(dm[:, 1]),
                              np.mean(dm[:, 2])]) / 10.

    os.chdir('../')

print mean_dm
