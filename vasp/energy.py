energies = list()
with open("OUTCAR", "r") as file :
	for line in file :
		if "energy(sigma->0)" in line :
			energies.append(line.split()[-1])
energy = energies[-1]
print(energy)
