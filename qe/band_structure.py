"""
Class for reading and plotting band structures
"""
import ast
import bz2
import csv

import matplotlib.pyplot as plt
import numpy
import pandas as pandas
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from tqdm import tqdm


class BandStructure:
    """
Class for representing band structures
    """

    def __init__(self, band_structure_path, fermi_energy_path):
        self.band_structure_path = band_structure_path
        self.fermi_energy_path = fermi_energy_path
        self.band_structure = []
        self.fermi_energy = None
        self.k_points = None
        self.bands = None
        self.projections_path = None
        self.atomic_states = pandas.DataFrame()
        self.number_of_bands = None
        self.number_of_k_points = None
        self.projections = []
        self.state_list = []
        self.projection_sums = []
        self.state_dictionary = {}
        self.color_array = []

    def get_fermi_energy(self):
        """
Get Fermi energy from fermi_energy_path
        """
        f = bz2.open(self.fermi_energy_path, 'rt').readlines()
        self.fermi_energy = float([x.split()[-2] for x in f
                                   if 'the Fermi energy is' in x][-1])

    def read_band_structure(self):
        """
Read band structure from <prefix>.bands.gnu located at band_structure_path
        """
        # get fermi energy
        if self.fermi_energy is None:
            self.get_fermi_energy()

        # get band structure
        if self.band_structure:
            return
        with bz2.open(self.band_structure_path, 'rt') as f:
            band = []  # initialize band as empty list
            for line in f:
                if len(line.split()) != 2:
                    self.band_structure.append(band)
                    band = []
                else:
                    band.append([float(x) for x in line.split()])

        # shift band energies by Fermi energy
        self.band_structure = numpy.array(self.band_structure)
        self.band_structure[:, :, 1] -= self.fermi_energy
        self.k_points = self.band_structure[:, :, 0].T
        self.bands = self.band_structure[:, :, 1].T

    def plot_band_structure(self, k_paths, path_lengths, y_limits,
                            save_plot=True):
        """
Plot band structure
        """
        plt.plot(self.k_points, self.bands, color='black')
        plt.ylabel(r'$E-E_{F}$ (eV)')
        if k_paths:
            if path_lengths:
                k_indices = numpy.cumsum(path_lengths)
                special_k = [x for i, x in enumerate(self.k_points[:, 0])
                             if i in k_indices]
                plt.xticks(special_k, k_paths)
                plt.grid(axis='x')
                plt.xlim(special_k[0], special_k[-1])
        if y_limits:
            plt.ylim(y_limits)
        if save_plot:
            plt.savefig('band_structure.pdf')
        else:
            plt.show()
        plt.close()

    def get_atomic_states(self):
        """
Get atomic states from projected density of states output
        """
        f = bz2.open(self.projections_path, 'rt').readlines()
        states = [x for x in f if 'state #' in x]
        for x in states:
            self.atomic_states = self.atomic_states.append({
                'state_number': int(x[12:16]),
                'atom_number': int(x[22:27]),
                'symbol': x[28:31].strip(),
                'wave_function_number': int(x[37:41]),
                'j': float(x[44:48]),
                'l': int(x[50:52]),
                'm_j': float(x[56:60])}, ignore_index=True)
        self.atomic_states.to_csv('atomic_states.csv', index=False)

    def read_projections(self, projections_path):
        """
Read atomic orbital projections from projected density of states output
        """
        self.projections_path = projections_path
        self.get_atomic_states()
        self.number_of_bands = self.band_structure.shape[0]
        self.number_of_k_points = self.band_structure.shape[1]
        with bz2.open(projections_path, 'rt') as f:
            for _ in tqdm(range(self.number_of_k_points)):

                # find next k-point
                for line in f:
                    if ' k =' in line:
                        break

                band_projections = []
                for _ in range(self.number_of_bands):
                    for index, line in enumerate(f):
                        if '    |psi|^2 =' in line:
                            break
                        elif index == 0:
                            energy = float(line.split()[4])
                        else:

                            # remove 'psi = ' and split on '+'
                            projections = line.replace('psi =', '').split('+')

                            # remove leading and trailing whitespace
                            # characters
                            projections = [x.strip() for x in projections]

                            # remove empty strings
                            projections = [x for x in projections if x != '']

                            # split on '*'
                            projections = [x.split('*') for x in projections]

                            # remove '[#' and ']' from state numbers
                            state_numbers = [
                                x.replace('[#', '').replace(']', '').strip()
                                for _, x in projections]

                            # recombine projections and state numbers as 
                            # floats and integers, respectively
                            projections = [
                                [float(x[0]), int(y)]
                                for x, y in zip(projections, state_numbers)]

                            if index == 1:
                                multiline_projections = projections
                            else:
                                multiline_projections += projections
                    band_projections.append(multiline_projections)
                self.projections.append(band_projections)

    def group_projections(self):
        """
Group projections by element and l quantum number
        """
        for k_index in tqdm(range(self.number_of_k_points)):
            band_projection_sums = []
            for band_index in range(self.number_of_bands):
                formatted_projections = []
                for x in self.projections[k_index][band_index]:
                    coefficient = x[0]
                    state_number = x[1]
                    state = ' '.join(self.atomic_states.loc[
                                         self.atomic_states[
                                             'state_number'] == state_number,
                                         ['symbol', 'l']].values.astype(str)[
                                         0])
                    if state not in self.state_list:
                        self.state_list.append(state)
                    formatted_projections.append([coefficient, state])
                dataframe = pandas.DataFrame(formatted_projections,
                                             columns=['coefficient', 'state'])

                # group by state and sum projections
                dataframe = dataframe.groupby(by='state').sum()
                states = dataframe.index.values
                sums = dataframe.values.flatten()
                band_projection_sums.append([[x, y]
                                             for x, y in zip(states, sums)])
            self.projection_sums.append(band_projection_sums)

        # write states list to csv
        with open('states_list.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.state_list)

        # write projection sums to csv
        with open('projection_sums.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.projection_sums)

    def load_projections(self, states_path, path):
        """
Load states list and projections from csv file
        """
        with open(states_path) as f:
            reader = csv.reader(f)
            for row in reader:
                symbol = ''.join(row[0:2])
                l_quantum_number = ''.join(row[3:])
                self.state_list.append(' '.join([symbol, l_quantum_number]))

        with open(path) as f:
            reader = csv.reader(f)
            for row in reader:
                row_sums = []
                for x in row:
                    row_sums.append(ast.literal_eval(x))
                self.projection_sums.append(row_sums)

    def get_color_array(self):
        """
Get color array
        """
        for k_index in range(self.number_of_k_points):
            band_colors = []
            for band_index in range(self.number_of_bands):
                color_sum = numpy.zeros(3)
                for index, projection_sum in enumerate(
                        self.projection_sums[k_index][band_index]):
                    color = to_rgb(self.state_dictionary[projection_sum[0]])
                    color_sum += numpy.array(color) * projection_sum[1]
                band_colors.append(color_sum)
            self.color_array.append(band_colors)
        self.color_array = numpy.array(self.color_array)

    def plot_projected_band_structure(self, k_paths, path_lengths,
                                      y_limits, colors, alpha, save_plot=True):
        """
Plot projected band structure
        """
        # get color array
        self.state_dictionary = dict(zip(self.state_list, colors))
        self.get_color_array()

        # plot band structure
        plt.plot(self.k_points, self.bands, color='black')

        # plot projections
        for index in range(self.number_of_bands):
            plt.scatter(self.k_points[:, index], self.bands[:, index],
                        color=self.color_array[:, index, :], alpha=alpha)

        # format plot
        plt.ylabel(r'$E-E_{F}$ (eV)')
        if k_paths:
            if path_lengths:
                k_indices = numpy.cumsum(path_lengths)
                special_k = [x for i, x in enumerate(self.k_points[:, 0])
                             if i in k_indices]
                plt.xticks(special_k, k_paths)
                plt.grid(axis='x')
                plt.xlim(special_k[0], special_k[-1])
        if y_limits:
            plt.ylim(y_limits)

        # add legend
        legend = [Line2D([0], [0], marker='o', color=value, label=key)
                  for key, value in self.state_dictionary.items()]
        plt.legend(bbox_to_anchor=(0, 1.02, 1, 0.102), handles=legend,
                   loc='lower_left', borderaxespad=0, ncol=4, mode='expand')

        if save_plot:
            plt.savefig('projected_band_structure.pdf')
        else:
            plt.show()
        plt.close()
