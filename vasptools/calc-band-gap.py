import sys
import numpy as np

with open("OUTCAR", "r") as file :
	for line in file :
		if "NBANDS=" in line :
			nbands = int(line.split()[-1])
			nkpts = int(line.split()[3])
			break

nsteps = 0
with open("OSZICAR", "r") as file :
	for line in file :
		if "E0" in line :
			nsteps += 1
nsteps *= 2 # currently this is a quick fix for spin-polarized calculations of non-magnetic systems

bs = np.zeros((nkpts, nbands, 2))
with open("OUTCAR", "r") as file :
	for i in range(nsteps) :
		for line in file :
			if "spin component" in line :
				break
	for ik in range(nkpts) :
		for line in file :
			if "k-point" in line :
				break
		next(file)
		for ib in range(nbands) :
			for line in file :
				bs[ik, ib, :] = line.split()[1:]
				break

filled = bs[:, :, 1] == 1
empty = bs[:, :, 1] == 0
bs_filled = bs[filled]
bs_empty = bs[empty]
bs_filled_evals = bs_filled[:, 0]
bs_empty_evals = bs_empty[:, 0]
homo = np.max(bs_filled_evals)
lumo = np.min(bs_empty_evals)
egap = lumo - homo
print("Band gap is {} eV".format(egap))
