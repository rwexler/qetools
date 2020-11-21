#!/usr/bin/env python
""" Utility functions """

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'

import bz2


def get_fermi_energy(path):
    """
Gets Fermi energy in eV from Quantum Espresso output files
    """
    fermi_energy = None
    if '.bz2' in path:
        file = bz2.open(path, 'rt')
    else:
        file = open(path)
    for line in file:
        if 'the Fermi energy is' in line:
            fermi_energy = float(line.split()[4])
            break
    file.close()
    return fermi_energy
