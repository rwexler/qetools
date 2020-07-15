#!/usr/bin/env python
"""
Program for getting the final total energy extrapolated to zero smearing
"""

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'


def main():
    """
Main program
    """
    with open('OUTCAR') as f:
        for line in f:
            if 'energy(sigma->0)0' in line:
                energy = line.split()[-1]
    print(energy)


if __name__ == '__main__':
    main()
