import sys
from glob import glob
import os
import numpy as np

prefix = sys.argv[1]
input = prefix + '.in'
contents = glob(input)
if contents :
    os.system('mv ' + input + ' ' + input + '.old')
input += '.old'
output = prefix + '.out'
new_qe_input = prefix + '.in'
nat = int(os.popen('grep nat ' + input).read().split()[2][:-1])
coords = np.array(os.popen('grep ATOMIC_POSITIONS -A ' + str(nat) + ' ' + output + ' | tail -' + str(nat)).read().split()).reshape((nat, 4))
elem_list = coords[:, 0].tolist()
coords = coords[:, 1:].astype(float)

def make_qe_input(filename, elem_list, coords) :
    with open(new_qe_input, 'w') as new :
        with open(input, 'r') as old :
            for line in old :
                if 'ATOMIC_POSITIONS' in line :
                    new.write(line)
                    break
                else :
                    new.write(line)
            for i, row in enumerate(coords) :
                new.write(elem_list[i] + ' ' +
                          str(row[0]) + ' ' +
                          str(row[1]) + ' ' +
                          str(row[2]) + '\n')

make_qe_input(new_qe_input, elem_list, coords)
os.system('qsub runscript')
