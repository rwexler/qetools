import numpy as np
# get number of ions
with open("OUTCAR", "r") as file :
	for line in file :
		if "NIONS" in line :
			nions = int(line.split()[-1])
			break
# get number of ionic steps
nsteps = 0
with open("OUTCAR", "r") as file :
	for line in file :
		if "TOTAL-FORCE" in line :
			nsteps += 1
# get forces
forces = list()
with open("OUTCAR", "r") as file :
	for i in range(nsteps) :
		for line in file :
			if "TOTAL-FORCE" in line :
				break
		next(file)
		for j in range(nions) :
			for line in file :
				forces.append(line.split()[-3:])
				break
forces = np.array(forces).astype(float)[-nions:]
print(forces)
