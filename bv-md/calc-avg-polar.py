import os
import numpy as np
nlines = int(os.popen('wc -l files.DM').read().split()[0])
command = 'cut -b 10- files.DM'
polar = np.array(os.popen(command).read().split()).reshape((nlines, 3)).astype(float)
mean = np.mean(polar, 0)
print mean[0], mean[1], mean[2]
