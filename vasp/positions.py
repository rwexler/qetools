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
		if "POSITION" in line :
			nsteps += 1
# get forces
positions = list()
with open("OUTCAR", "r") as file :
	for i in range(nsteps) :
		for line in file :
			if "POSITION" in line :
				break
		next(file)
		for j in range(nions) :
			for line in file :
				positions.append(line.split()[:3])
				break
positions = np.array(positions).astype(float)[-nions:]
print(positions)
