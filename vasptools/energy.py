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
    f = open('OUTCAR').readlines()
    print([x.split()[-1] for x in f if 'energy(sigma->0)' in x][-1])


if __name__ == '__main__':
    main()
