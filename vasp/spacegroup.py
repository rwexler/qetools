from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from ase.io import read
from pymatgen.io.ase import AseAtomsAdaptor

s_ase = read("OUTCAR", format = "vasp-out")
s_pmg = AseAtomsAdaptor().get_structure(s_ase)
space_group_number = SpacegroupAnalyzer(s_pmg).get_space_group_number()
space_group_symbol = SpacegroupAnalyzer(s_pmg).get_space_group_symbol()
print("{} ({})".format(space_group_symbol, space_group_number))
