#!/usr/bin/env python
"""
Program for getting the lattice constants
"""

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'

import sys

BOHR_TO_ANGSTROM = 0.529177210903
OUTPUT = sys.argv[1]


def get_number_of_cells():
    """
Get number of cells in calculation
    """
    f = open(OUTPUT).readlines()
    return sum([1 for x in f if 'CELL_PARAMETERS' in x])


def get_cell_parameters(number_of_cells):
    """
Get cell parameters
    """
    with open(OUTPUT) as f:
        cell_parameters = []
        for i in range(number_of_cells):
            for line in f:
                if 'CELL_PARAMETERS' in line:
                    break
            for j in range(3):
                for line in f:
                    cell_parameters.append(line.split())
                    break
    return cell_parameters[-3:]


def get_crystal_axes():
    """
Get cell dimensions and crystal axes
    """
    # get cell dimensions 1, i.e., alat
    with open(OUTPUT) as f:
        for line in f:
            if 'celldm(1)=' in line:
                alat = float(line.split()[1]) * BOHR_TO_ANGSTROM
                break

    # get crystal axes
    crystal_axes = []
    with open(OUTPUT) as f:
        for line in f:
            if 'crystal axes:' in line:
                break
        for i in range(3):
            for line in f:
                crystal_axes.append(
                    [float(x) * alat for x in line.split()[3:6]])
                break
    return crystal_axes


def main():
    """
Main program
    """
    number_of_cells = get_number_of_cells()
    number_of_cells = 0
    if number_of_cells >= 1:
        lattice_vectors = get_cell_parameters(number_of_cells)
        for x in lattice_vectors:
            print('{} {} {}'.format(x[0], x[1], x[2]))
    else:
        lattice_vectors = get_crystal_axes()
        for x in lattice_vectors:
            print('{:9.6f} {:9.6f} {:9.6f}'.format(x[0], x[1], x[2]))


if __name__ == '__main__':
    main()
