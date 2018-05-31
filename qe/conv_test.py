import os
import numpy as np

filename = "asn.in"
values = np.arange(30, 75, 5)

old_file = open(filename, "r")

for value in values :
    dir = str(value)
    os.system("mkdir -p " + dir)
    os.chdir(dir)

    new_file = open(filename, "w")
    for line in old_file :
        if "ecutwfc" in line :
            new_file.write("ecutwfc = " + str(value) + ",\n")
            break
        else :
            new_file.write(line)
    
    for line in old_file :
        new_file.write(line)

    os.system("cp ../runscript ./")
    os.system("cp ../*.upf ./")
    os.system("qsub runscript")

    old_file.seek(0)

    os.chdir('../')

old_file.close()
new_file.close()
