import sys
import numpy as np

filename = sys.argv[1]

with open(filename, "r") as vasp :
    # read vasp file
    next(vasp); next(vasp)
    lvs = list()
    for i in range(3) :
        for line in vasp :
            lvs.append(line.split())
            break
    lvs = np.array(lvs).astype(float)
    for line in vasp :
        elems = line.split()
        break
    nelems = list()
    for line in vasp :
        for item in line.split() :
            nelems.append(int(item))
        break
    elem_list = list()
    for elem, nelem in zip(elems, nelems) :
        elem_list += [elem] * nelem
    next(vasp)
    coords = list()
    for line in vasp :
        coords.append(line.split())
    coords = np.array(coords).astype(float)
    
    # make xsf file
    with open(filename[:-11] + "xsf", "w") as xsf :
        xsf.write("CRYSTAL\nPRIMVEC\n")
        for row in lvs :
            xsf.write("{: 14.9f} {: 13.9f} {: 13.9f}\n".format(row[0], row[1], row[2]))
        xsf.write("PRIMCOORD\n" + str(coords.shape[0]) + "\n")
        for elem, coord in zip(elem_list, coords) :
            xsf.write("{:2} {: 17.9f} {: 13.9f} {: 13.9f}\n".format(elem, coord[0], coord[1], coord[2]))
