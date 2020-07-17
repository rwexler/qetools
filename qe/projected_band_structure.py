#!/usr/bin/env python
"""
Program for plotting atomic-orbital-projected band structures
"""

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'

from band_structure import BandStructure

# BAND STRUCTURE PARAMETERS
ROOT = '/Users/robertwexler/Dropbox (Princeton)/band-inversions/BaAgBi'
BAND_STRUCTURE = ROOT + '/bands/qe.bands.gnu.bz2'
FERMI_ENERGY = ROOT + '/fr-scf/qe.out.bz2'
K_PATHS = [r'$\Gamma$', 'K', 'M', r'$\Gamma$', 'A', 'H', 'L', 'A']
PATH_LENGTHS = [0, 47, 37, 50, 50, 47, 37, 50]
Y_LIMITS = [-2, 2]

# PROJECTED BAND STRUCTURE PARAMETER
PROJECTIONS = ROOT + '/pdos/qe.out.bz2'
COLORS = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black',
          'white']
ALPHA = 0.1


def main():
    """
Main program
    """
    # plot band structure
    bs = BandStructure(BAND_STRUCTURE, FERMI_ENERGY)
    bs.read_band_structure()
    bs.plot_band_structure(K_PATHS, PATH_LENGTHS, Y_LIMITS)

    # plot projected band structure
    bs.read_projections(PROJECTIONS)
    bs.group_projections()
    # bs.load_projections('states_list.csv', 'projection_sums.csv')
    bs.plot_projected_band_structure(K_PATHS, PATH_LENGTHS, Y_LIMITS, COLORS,
                                     ALPHA)


if __name__ == '__main__':
    main()
