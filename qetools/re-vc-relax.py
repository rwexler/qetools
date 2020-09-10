import sys
import os
import numpy as np

filename = sys.argv[1]

# get number of atoms
nat = int(os.popen("grep 'number of atoms' " + filename).read().split()[4])

# get lattice vectors
lvs = os.popen("grep CELL -A 3 " + filename + " | grep -v CELL | grep -v -- '^--$'").read().split()
nstr = len(lvs) / 9
lvs = np.array(lvs).reshape((nstr, 3, 3))

# get coordinates
coords = os.popen("grep ATOM -A " + str(nat) + " " + filename + " | grep -v ATOM | grep -v -- '^--$'").read().split()
coords = np.array(coords).reshape((nstr, nat, 4))

new_lvs = lvs[-1]
new_coords = coords[-1]

# generate new qe input file
with open(filename[:-3] + "in.old", "r") as old :
	with open(filename[:-3] + "in", "w") as new :
		for line in old :
			if "CELL_PARAMETERS" in line :
				new.write(line)
				break
			else :
				new.write(line)
		for row in new_lvs :
			new.write(row[0] + " " + row[1] + " " + row[2] + "\n")
		next(old); next(old); next(old)
		for line in old :
			if "ATOMIC_POSITIONS" in line :
				new.write(line)
				break
			else :
				new.write(line)
		for row in new_coords :
			new.write(row[0] + " " + row[1] + " " + row[2] + " " + row[3] + "\n")

os.system("qsub runscript")
