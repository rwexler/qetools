#!/usr/bin/env python
"""
Module containing classes for parsing densities of states
"""

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'

import bz2
from glob import glob

import numpy as np


class ParseDensityOfStates:
    """
Class for parsing outputs of Quantum Espresso projected density of
states calculations

Can read both compressed (bzip2) and uncompressed (txt) files

Can parse both open- and closed-shell densities of states
    """

    def __init__(self, path, indices, weights, projected=True, spin=True):
        self.path = path

        # Quantum Espresso uses one-based numbering
        self.indices = [x + 1 for x in indices]

        self.weights = weights
        self.projected = projected
        self.spin = spin
        self.paths = []
        self.s_paths = None
        self.p_paths = None
        self.d_paths = None
        self.f_paths = None
        self.s_density_of_states = None
        self.p_density_of_states = None
        self.d_density_of_states = None
        self.f_density_of_states = None
        self.density_of_states = None
        self.number_of_energies = None
        self.energies = None
        self.relative_energies = None
        self.fermi_energy = None

    def get_paths(self):
        """
Gets paths to outputs
        """
        for index, weight in zip(self.indices, self.weights):
            self.paths += [[x, weight] for x in sorted(glob(
                self.path + '*atm#' + str(index) + '(*'))]
        if self.projected:
            self.s_paths = [[x, y] for x, y in self.paths if '(s)' in x]
            self.p_paths = [[x, y] for x, y in self.paths if '(p)' in x]
            self.d_paths = [[x, y] for x, y in self.paths if '(d)' in x]
            self.f_paths = [[x, y] for x, y in self.paths if '(f)' in x]

    def get_number_of_energies(self, path):
        """
Gets number of energies in projected density of states
        """
        self.number_of_energies = 0
        if '.bz2' in path:
            file = bz2.open(path, 'rt')
        else:
            file = open(path)
        next(file)
        for line in file:
            # Quantum Espresso writes '*******' whenever the energy
            # has more than six digits
            if '*******' not in line:
                self.number_of_energies += 1
        file.close()

    def get_projected_density_of_states(self, path):
        """
Gets projected density of states
        """
        l_quantum_number = path.split('#')[-1].split('(')[-1].split(')')[0]
        if self.spin:
            number_of_columns = {'s': 5, 'p': 9, 'd': 13, 'f': 17}
        else:
            number_of_columns = {'s': 3, 'p': 5, 'd': 7, 'f': 9}
        if self.number_of_energies is None:
            self.get_number_of_energies(path)
        projected_density_of_states = np.zeros((
            self.number_of_energies, number_of_columns[l_quantum_number]))
        if '.bz2' in path:
            file = bz2.open(path, 'rt')
        else:
            file = open(path)
        next(file)
        index = 0
        for line in file:
            if '*******' not in line:
                projected_density_of_states[index, :] = line.split()
                index += 1
        file.close()
        return projected_density_of_states.astype(float)

    def sum_projected_densities_of_states(self, paths):
        """
Sums projected densities of states
        """
        projected_density_of_states_sum = None
        for index, path in enumerate(paths):
            projected_density_of_states = \
                self.get_projected_density_of_states(path[0])
            if self.energies is None:
                self.energies = projected_density_of_states[:, 0]
            if projected_density_of_states_sum is None:
                projected_density_of_states_sum = \
                    projected_density_of_states[:, 1:3] * path[1]
            else:
                projected_density_of_states_sum += \
                    projected_density_of_states[:, 1:3] * path[1]
        return projected_density_of_states_sum

    def get_densities_of_states(self):
        """
Gets densities of states by summing projected densities of states
        """
        self.get_paths()
        if self.projected:
            self.s_density_of_states = self.sum_projected_densities_of_states(
                self.s_paths)
            self.p_density_of_states = self.sum_projected_densities_of_states(
                self.p_paths)
            self.d_density_of_states = self.sum_projected_densities_of_states(
                self.d_paths)
            self.f_density_of_states = self.sum_projected_densities_of_states(
                self.f_paths)
        else:
            self.density_of_states = self.sum_projected_densities_of_states(
                self.paths)

    def calculate_relative_energies(self, fermi_energy):
        """ Calculates energies relative to the Fermi energy """
        self.relative_energies = self.energies - fermi_energy
        self.fermi_energy = fermi_energy
