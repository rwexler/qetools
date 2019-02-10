import sys
import os
import numpy as np

prefix = sys.argv[1]
input = prefix + '.in'
output = prefix + '.out'
xsf_filename = prefix + '.xsf'
calculation = os.popen('grep calculation ' + input).read().split("'")[1]
nat = int(os.popen('grep nat ' + input).read().split()[2][:-1])
lvs = np.array(os.popen('grep CELL_PARAMETERS -A 3 ' + input + ' | grep -v CELL_PARAMETERS').read().split()).reshape((3, 3)).astype(float)

def make_xsf(filename, lvs, nat, elem_list, coords) :
    with open(filename, 'w') as xsf :
        xsf.write('CRYSTAL\nPRIMVEC\n')
        for row in lvs :
            xsf.write(str(row[0]) + ' ' +
                      str(row[1]) + ' ' +
                      str(row[2]) + '\n')
        xsf.write('PRIMCOORD\n' + str(nat) + '\n')
        for i, row in enumerate(coords) :
            xsf.write(elem_list[i] + ' ' +
                      str(row[0]) + ' ' +
                      str(row[1]) + ' ' +
                      str(row[2]) + '\n')

if calculation == 'vc-relax' :
    lvs = np.array(os.popen('grep CELL_PARAMETERS -A 3 ' + output + ' | tail -3').read().split()).reshape((3, 3)).astype(float)
    coords = np.array(os.popen('grep ATOMIC_POSITIONS -A ' + str(nat) + ' ' + output + ' | tail -' + str(nat)).read().split()).reshape((nat, 4))
    elem_list = coords[:, 0].tolist()
    coords = coords[:, 1:].astype(float)
    make_xsf(xsf_filename, lvs, nat, elem_list, coords)
elif calculation == 'relax' :
    coords = np.array(os.popen('grep ATOMIC_POSITIONS -A ' + str(nat) + ' ' + output + ' | tail -' + str(nat)).read().split()).reshape((nat, 4))
    elem_list = coords[:, 0].tolist()
    coords = coords[:, 1:].astype(float)
    make_xsf(xsf_filename, lvs, nat, elem_list, coords)
