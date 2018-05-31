import sys
import os
import numpy as np

per_uc = 5
avg_rng = 1000 # average over last 1000 values

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

for i, dir in enumerate(dirs) :

    os.chdir(dir)

    # get number of steps
    nsteps = int(os.popen('grep "#" files.PbO.dat | wc -l').read()) - 2

    # get displacements
    nhead = str(nsteps * (nasite + 1))
    ntail = str(avg_rng * (nasite + 1))
    nrows = avg_rng * nasite
    disp = np.array(os.popen('head -' + nhead + ' files.PbO.dat | tail -' + ntail + ' | grep -v "#" | cut -b 5-').read().split()).reshape((nrows, 3)).astype(float)

    # get average displacements
    av_disp = disp.mean(0)
    print int(dir[2:-1]), av_disp[0], av_disp[1], av_disp[2]

    os.chdir('../')
