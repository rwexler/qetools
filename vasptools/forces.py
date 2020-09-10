#!/usr/bin/env python
""" 
Program for getting the final forces
"""

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'


def get_number_of_ions():
    """
Get number of ions from OUTCAR
    """
    f = open('OUTCAR').readlines()
    return int([x.split()[-1] for x in f if 'NIONS' in x][-1])


def get_number_of_steps():
    """
Get number of ionic steps from OUTCAR
    """
    f = open('OUTCAR').readlines()
    return int(sum([1 for x in f if 'TOTAL-FORCE' in x]))


def get_forces(number_of_steps, number_of_ions):
    """
Get forces from OUTCAR
    """
    forces = []
    with open('OUTCAR') as f:
        for _ in range(number_of_steps):
            for line in f:
                if 'TOTAL-FORCE' in line:
                    break
            next(f)
            for _ in range(number_of_ions):
                for line in f:
                    forces.append([float(x) for x in line.split()[-3:]])
                    break
    return forces


def main():
    """
Main program
    """
    number_of_ions = get_number_of_ions()
    number_of_steps = get_number_of_steps()
    forces = get_forces(number_of_steps, number_of_ions)
    for x in forces[-number_of_ions:]:
        print('{: .6f} {: .6f} {: .6f}'.format(x[0], x[1], x[2]))


if __name__ == '__main__':
    main()
