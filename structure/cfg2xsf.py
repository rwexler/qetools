import sys
import numpy as np

filename = sys.argv[1]

with open(filename, "r") as file :

    # read number of particles
    for line in file :
        npart = int(line.split()[4])
        break
        
    # read lattice vectors
    lvs = list()
    next(file); next(file)
    for i in range(9) :
        for line in file :
            lvs.append(float(line.split()[2]))
            break
    lvs = np.array(lvs).reshape((3, 3))

    # read atomic coordinates
    elems = list()
    coords = list()
    next(file); next(file); next(file)
    for line in file :
        if ("Sr" in line) or ("Ti" in line) or ("O" in line) :
            cur_elem = line.split()[0]
        elif len(line.split()) > 1 :
            elems.append(cur_elem)
            coords.append(line.split()[:3])
    coords = np.array(coords).astype(float)
    
    # convert fractional coordinates to angstroms
    lcs = np.linalg.norm(lvs, axis = 1)
    coords *= lcs
    
    # write xsf file
    with open(filename[:-3] + "xsf", "w") as xsf :
        xsf.write("CRYSTAL\nPRIMVEC\n")
        for lv in lvs :
            xsf.write('{: 14.9f} {: 13.9f} {: 13.9f}\n'.format(lv[0], lv[1], lv[2]))
        xsf.write("PRIMCOORD\n" + str(npart) + " 1\n")
        for elem, coord in zip(elems, coords) :
            xsf.write('{:2} {: 17.9f} {: 13.9f} {: 13.9f}\n'.format(elem, coord[0], coord[1], coord[2]))
