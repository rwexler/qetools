#!/usr/bin/env python
"""
Program for plotting atomic-orbital-projected band structures
"""

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'

import sys
from shutil import copyfile

INPUT = sys.argv[1]


def get_number_of_atoms(input):
    """
Get number of atoms from input file
    """
    f = open(input).readlines()
    return int([x.split()[-1].replace(',', '') for x in f if 'nat' in x][-1])


def main():
    """
Main program
    """
    old_input = INPUT + '.old'
    copyfile(INPUT, old_input)
    number_of_atoms = get_number_of_atoms(old_input)
    print(number_of_atoms)


if __name__ == '__main__':
    main()

from glob import glob
import os
import numpy as np

prefix = sys.argv[1]
input = prefix + '.in'
contents = glob(input)
if contents:
    os.system('mv ' + input + ' ' + input + '.old')
input += '.old'
output = prefix + '.out'
new_qe_input = prefix + '.in'
nat = int(os.popen('grep nat ' + input).read().split()[2][:-1])
coords = np.array(os.popen(
    'grep ATOMIC_POSITIONS -A ' + str(nat) + ' ' + output + ' | tail -' + str(
        nat)).read().split()).reshape((nat, 4))
elem_list = coords[:, 0].tolist()
coords = coords[:, 1:].astype(float)


def make_qe_input(filename, elem_list, coords):
    with open(new_qe_input, 'w') as new:
        with open(input, 'r') as old:
            for line in old:
                if 'ATOMIC_POSITIONS' in line:
                    new.write(line)
                    break
                else:
                    new.write(line)
            for i, row in enumerate(coords):
                new.write(elem_list[i] + ' ' +
                          str(row[0]) + ' ' +
                          str(row[1]) + ' ' +
                          str(row[2]) + '\n')


make_qe_input(new_qe_input, elem_list, coords)
os.system('qsub runscript')
