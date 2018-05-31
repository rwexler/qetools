import os
import numpy as np
inputfilename = "asn.in"
inputfile = open(inputfilename,"r")

# read lattice vectors
for line in inputfile:
    if "CELL_PARAMETERS" in line:
        break
a = np.zeros(3)
b = np.zeros(3)
c = np.zeros(3)
for line in inputfile:
    list = line.split()
    for i in range(len(list)):
        a[i] = float(list[i])
    break
for line in inputfile:
    list = line.split()
    for    i in range(len(list)):
        b[i] = float(list[i])
    break
for line in inputfile:
    list = line.split()
    for    i in range(len(list)):
        c[i] = float(list[i])
    break
inputfile.seek(0)

# read atomic positions in crystal coordinates
positionsfilename = "positions.dat"
positionsfile = open(positionsfilename,"r")

nat = 0
for line in positionsfile:
    nat += 1
positionsfile.seek(0)

elements = []
positions = np.zeros((3,nat))
i = 0
for line in positionsfile:
    list = line.split()
    elements.append(list[0])
    positions[0,i] = float(list[1])
    positions[1,i] = float(list[2])
    positions[2,i] = float(list[3])
    i += 1

#
initial = -0.04
final = 0.04
step = 0.01
grid = np.arange(initial,final+step,step)

for i in range(len(grid)):
    print("Grid value: "+str(grid[i]))
    
    # calculate new lattice constants
    a_new = a + grid[i]*a
    b_new = b + grid[i]*b
    c_new = c + grid[i]*c
    print("a = "+str(a_new[0])+" i + "+str(a_new[1])+" j + "+str(a_new[2])+" k")
    print("b = "+str(b_new[0])+" i + "+str(b_new[1])+" j + "+str(b_new[2])+" k")
    print("c = "+str(c_new[0])+" i + "+str(c_new[1])+" j + "+str(c_new[2])+" k")

    # calculate new volumes
    cell_parameters = np.vstack((a_new, b_new, c_new))
    print("Volume = "+str(np.linalg.det(cell_parameters)))

    # make directory
    if grid[i] < 0:
        directoryname = "n"+str(grid[i])[1:]
    else:
        directoryname = str(grid[i])
    print("Directory Name: "+directoryname)
    os.system("mkdir "+directoryname)
    os.chdir(directoryname)

    # copy in files
    os.system("cp ../*.upf ../runscript ./")
    
    # make new input file
    newinputfile = open(inputfilename,"w")
    for line in inputfile:
        newinputfile.write(line)
        if "CELL_PARAMETERS" in line:
            break
    inputfile.seek(0)
    newinputfile.write(str(a_new[0])+" "+str(a_new[1])+" "+str(a_new[2])+"\n")
    newinputfile.write(str(b_new[0])+" "+str(b_new[1])+" "+str(b_new[2])+"\n")
    newinputfile.write(str(c_new[0])+" "+str(c_new[1])+" "+str(c_new[2])+"\n")
    newinputfile.write("\n")
    newinputfile.write("ATOMIC_POSITIONS (crystal)\n")
    for j in range(nat):
        newinputfile.write(elements[j]+" "+
                           str(positions[0,j])+" "+
                           str(positions[1,j])+" "+
                           str(positions[2,j])+"\n")
    newinputfile.close()

    # submit calculations
    os.system("qsub runscript")

    # return to parent directory
    os.chdir("../")
