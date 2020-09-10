import numpy as np
from pymatgen.core.structure import Structure
import os

structure = Structure.from_file("POSCAR")
strains = np.arange(-10, 11) / 100.
cwd = os.getcwd()
for i, strain in enumerate(strains) :
    new_structure = structure.copy()
    new_structure.apply_strain(strain)
    directory = "{:02d}={:+3.2f}".format(i, strain)
    os.system("mkdir -p {}".format(directory))
    os.chdir(directory)
    new_structure.to("vasp", "POSCAR")
    os.system("cp ../INCAR ../KPOINTS ../POTCAR ../runscript ./")
    os.system("sbatch runscript")
    os.chdir(cwd)
