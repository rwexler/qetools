import numpy as np
import sys

# definitions
rcut = 10                   # cutoff radius for application of periodic boundary conditions
restart = int(sys.argv[1])  # 0 = no, 1 = yes

# determine the number of time steps, i.e. nsteps
dumpfilename = "dump.lammpstrj"
dumpfile = open(dumpfilename,"r")
nsteps = 0
for line in dumpfile:
    if "ITEM: TIMESTEP" in line:
        nsteps += 1
dumpfile.seek(0)

# determine the time of each time step, i.e. step
step = []
for i in range(0,nsteps):
    for line in dumpfile:
        if "ITEM: TIMESTEP" in line:
            nxtline = dumpfile.next()
            list = nxtline.split()
            step.append(int(list[0]))

dumpfile.seek(0)

# is this a restarted simulation?
if restart == 1:
    sims = 2
else:
    sims = 3

# determine the lattice constants at each time step
logfilename = "files.log"
logfile = open(logfilename,"r")
steplat = []
alat = []
blat = []
clat = []
for i in range(0,sims):
    for line in logfile:
        if "Step Temp E_angle TotEng Press Volume Lx Ly Lz" in line:
            break
for line in logfile:
    if "Loop time of" in line:
        break
    list = line.split()
    steplat.append(int(list[0]))
    alat.append(float(list[6]))
    blat.append(float(list[7]))
    clat.append(float(list[8]))

# determine the number of atoms in the supercell, i.e. natoms
datafilename = "data.asn"
datafile = open(datafilename,"r")
for line in datafile:
    if "atoms" in line:
	list = line.split()
	natoms = int(list[0])
	break

# determine the molecule id, charges, and positions for each atom
for line in datafile:
    if "Atoms" in line:
        break
for line in datafile:
    break
molecules = np.zeros(natoms)
charges = np.zeros(natoms)
initial_positions = np.zeros((3,natoms))
for i in range(0,natoms):
    for line in datafile:
        list = line.split()
        molecules[i] = int(list[1])
	charges[i] = float(list[3])
	initial_positions[0,i] = float(list[4])
	initial_positions[1,i] = float(list[5])
	initial_positions[2,i] = float(list[6])
	break
datafile.close()

# read atom positions
size = (nsteps,3,natoms)
positions = np.zeros(size)
for i in range(0,nsteps):
    for line in dumpfile:
        if "ITEM: ATOMS id type x y z vx vy vz" in line:
            break
    for j in range(0,natoms):
        for line in dumpfile:
            list = line.split()
            positions[i,0,j] = float(list[2])
            positions[i,1,j] = float(list[3])
            positions[i,2,j] = float(list[4])
            break
dumpfile.close()

# apply periodic boundary conditions to complete each molecule

# make sure that the first entry in step and steplat are equal
for i in range(0,nsteps):
    if (steplat[i] == step[0]):
        eq_indx = i
        break
del steplat[0:eq_indx]
del alat[0:eq_indx]
del blat[0:eq_indx]
del clat[0:eq_indx]

# remove every other entry in steplat, alat, blat, and clat
steplat = steplat[0::2]
alat = alat[0::2]
blat = blat[0::2]
clat = clat[0::2]

# loop over each time step
for i in range(0,nsteps):

    # define lattice constants
    a = alat[i]
    b = blat[i]
    c = clat[i]

    start = 0
    # loop over each atom
    for j in range(0,natoms):
        
        # initial position of atom j
        initial_x = initial_positions[0,j]
        initial_y = initial_positions[1,j]
	initial_z = initial_positions[2,j]

        # current position of atom k
        current_x = positions[i,0,j]
        current_y = positions[i,1,j]
        current_z = positions[i,2,j]
        
        # calculate distance between temporary and mean position
	dist_x = current_x - initial_x
	dist_y = current_y - initial_y
	dist_z = current_z - initial_z
	
        # apply periodic boundary conditions
        if dist_x > rcut:
            current_x -= a
        if dist_x < -rcut:
            current_x += a
        if dist_y > rcut:
            current_y -= b
        if dist_y < -rcut:
            current_y += b
        if dist_z > rcut:
            current_z -= c
        if dist_z < -rcut:
            current_z += c
            
        positions[i,0,j] = current_x
        positions[i,1,j] = current_y
        positions[i,2,j] = current_z

# calculate total dipole moment as a function of time
outputname = "output.dat"
output = open(outputname,"w")
for i in range(0,nsteps):
    temp_x = positions[i,0,]
    temp_y = positions[i,1,]
    temp_z = positions[i,2,]
    dx = np.sum(charges*temp_x)
    dy = np.sum(charges*temp_y)
    dz = np.sum(charges*temp_z)
    string = str(i)+"     "+str(dx)+"     "+str(dy)+"     "+str(dz)+"\n"
    output.write(string)
output.close()

# calculate molecule dipole moments
