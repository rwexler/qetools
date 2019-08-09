import sys
from ase.io import read

filename = sys.argv[1]

stru = read(filename)
latcst = stru.get_cell_lengths_and_angles()
print(latcst)
