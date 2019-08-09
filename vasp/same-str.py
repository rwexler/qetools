import sys
from pymatgen import Structure
from pymatgen.analysis.structure_matcher import StructureMatcher

filenames = sys.argv[1:3]
old_str = Structure.from_file(filenames[0])
new_str = Structure.from_file(filenames[1])
same_str = print(StructureMatcher().fit(old_str, new_str))
