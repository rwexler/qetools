import sys
import os
import numpy as np

per_uc = 5
avg_rng = 1000 # average over last 1000 values
nbins = 600
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

# get b-sites
is_b_site = np.logical_or(typ_symb == 'Zr', typ_symb == 'Ti')
b_sites = typ_symb[is_b_site]

# get b-site list
b_site_list = np.tile(b_sites, avg_rng)
zr_indx = np.argwhere(b_site_list == 'Zr').flatten()
ti_indx = np.argwhere(b_site_list == 'Ti').flatten()

# get list of directories
from glob import glob
dirs = sorted([dir for dir in glob("./*") if 'K' in dir])
print 'directories = ', dirs

# get list of temperatures
temps = [int(dir[2:-1]) for dir in dirs]
print 'temperatures = ', temps

# initialize list of distributions
zr_dist_by_temp = list()
ti_dist_by_temp = list()

for i, dir in enumerate(dirs) :

    os.chdir(dir)

    # get number of steps
    nsteps = int(os.popen('grep "#" files.TiO.dat | wc -l').read()) - 2

    # get displacements
    nhead = str(nsteps * (nasite + 1))
    ntail = str(avg_rng * (nasite + 1))
    nrows = avg_rng * nasite
    disp = np.array(os.popen('head -' + nhead + ' files.TiO.dat | tail -' + ntail + ' | grep -v "#" | cut -b 5-').read().split()).reshape((nrows, 3)).astype(float)
    zr_disp = disp[zr_indx]
    ti_disp = disp[ti_indx]

    # get magnitude of displacements
    zr_disp_mag = np.sqrt(np.power(zr_disp[:, 0], 2) + np.power(zr_disp[:, 1], 2) + np.power(zr_disp[:, 2], 2))
    ti_disp_mag = np.sqrt(np.power(ti_disp[:, 0], 2) + np.power(ti_disp[:, 1], 2) + np.power(ti_disp[:, 2], 2))

    # get distribution of displacements
    zr_hist = np.histogram(zr_disp_mag, bins = nbins, range = (0.0, max_disp), density = True)
    ti_hist = np.histogram(ti_disp_mag, bins = nbins, range = (0.0, max_disp), density = True)

    # add data to list
    ## zr
    x = zr_hist[1]
    dx = x[1] - x[0]
    x += dx / 2.
    x = x[:-1]
    y = zr_hist[0]
    if i == 0 :
        zr_dist_by_temp.append(x)
        zr_dist_by_temp.append(y)
    else :
        zr_dist_by_temp.append(y)

    ## ti
    x = ti_hist[1]
    dx = x[1] - x[0]
    x += dx / 2.
    x = x[:-1]
    y = ti_hist[0]
    if i == 0 :
        ti_dist_by_temp.append(y)
    else :
        ti_dist_by_temp.append(y)

    print dir, 'done!'

    os.chdir('../')

zr_dist_by_temp = np.array(zr_dist_by_temp).transpose()
ti_dist_by_temp = np.array(ti_dist_by_temp).transpose()
np.savetxt("zr-dists.csv", zr_dist_by_temp, delimiter=",")
np.savetxt("ti-dists.csv", ti_dist_by_temp, delimiter=",")
