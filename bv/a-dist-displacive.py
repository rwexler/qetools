import sys
import os
import numpy as np

per_uc = 5
avg_rng = 1000 # average over last 1000 values
nbins = 1200
min_disp = -0.3
max_disp = 0.3

# get path to data file
path = sys.argv[1]
print 'path = ', path

# get number of atoms
nat = int(os.popen('grep atoms ' + path).read().split()[0])
nasite = nat / per_uc
print 'number of atoms = ', nat

# get initial structure information
str_init = np.array(os.popen('grep Atoms -A ' + str(nat + 1) + ' ' + path + ' | grep -v Atoms | grep -v -e "^$"').read().split()).reshape((nat, 7)).astype(float)
typ_indx = str_init[:, 2].astype(int)
print 'type indices = ', typ_indx

# get number of atom types
natyp = int(os.popen('grep "atom types" ' + path).read().split()[0])
print 'number of atom types = ', natyp

# get atom types
atyp = np.array(os.popen('grep Masses -A ' + str(natyp + 1) + ' ' + path + ' | grep -v Masses | grep -v -e "^$"').read().split()).reshape((natyp, 4))[:, 3]
typ_dict = {}
for i in typ_indx :
    typ_dict[i] = atyp[i - 1]
typ_symb = list()
for indx in typ_indx :
    typ_symb.append(typ_dict[indx])
typ_symb = np.array(typ_symb)
print 'type symbols = ', typ_symb

# get list of directories
from glob import glob
dirs = sorted([dir for dir in glob("./*") if 'K' in dir])
print 'directories = ', dirs

# get list of temperatures
temps = [int(dir[2:-1]) for dir in dirs]
print 'temperatures = ', temps

# initialize list of distributions
x_dist_by_temp = list()
y_dist_by_temp = list()
z_dist_by_temp = list()

for i, dir in enumerate(dirs) :

    os.chdir(dir)

    # get number of steps
    nsteps = int(os.popen('grep "#" files.PbO.dat | wc -l').read()) - 2

    # get displacements
    nhead = str(nsteps * (nasite + 1))
    ntail = str(avg_rng * (nasite + 1))
    nrows = avg_rng * nasite
    disp = np.array(os.popen('head -' + nhead + ' files.PbO.dat | tail -' + ntail + ' | grep -v "#" | cut -b 5-').read().split()).reshape((nrows, 3)).astype(float)

    # get components of displacements
    x_disp = disp[:, 0]
    y_disp = disp[:, 1]
    z_disp = disp[:, 2]

    # get distribution of displacements
    x_hist = np.histogram(x_disp, bins = nbins, range = (min_disp, max_disp), density = True)
    y_hist = np.histogram(y_disp, bins = nbins, range = (min_disp, max_disp), density = True)
    z_hist = np.histogram(z_disp, bins = nbins, range = (min_disp, max_disp), density = True)

    # add data to list
    x = x_hist[1]
    dx = x[1] - x[0]
    x += dx / 2.
    x = x[:-1]
    y_x = x_hist[0]
    y_y = y_hist[0]
    y_z = z_hist[0] 
    if i == 0 :
        x_dist_by_temp.append(x)
        y_dist_by_temp.append(x)
        z_dist_by_temp.append(x)
        x_dist_by_temp.append(y_x)
        y_dist_by_temp.append(y_y)
        z_dist_by_temp.append(y_z)
    else :
        x_dist_by_temp.append(y_x)
        y_dist_by_temp.append(y_y)
        z_dist_by_temp.append(y_z)

    print dir, 'done!'

    os.chdir('../')

x_dist_by_temp = np.array(x_dist_by_temp).transpose()
y_dist_by_temp = np.array(y_dist_by_temp).transpose()
z_dist_by_temp = np.array(z_dist_by_temp).transpose()
np.savetxt("x-dists-displacive.csv", x_dist_by_temp, delimiter=",")
np.savetxt("y-dists-displacive.csv", y_dist_by_temp, delimiter=",")
np.savetxt("z-dists-displacive.csv", z_dist_by_temp, delimiter=",")
