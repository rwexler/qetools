import sys
import os
import numpy as np

filename = sys.argv[1]
values = np.arange(2, 12, 2)

old_file = open(filename, "r")

for value in values :
    dir = str(value)
    if int(dir) < 10 :
        dir = "0" + dir
    os.system("mkdir -p " + dir)
    os.chdir(dir)

    new_file = open(filename, "w")
    for line in old_file :
        if "K_POINTS" in line :
            new_file.write(line)
            break
        else :
            new_file.write(line)
    for line in old_file :
        break
    new_file.write(str(value) + " " + str(value) + " " + str(value) + " 1 1 1\n")
    for line in old_file :
        new_file.write(line)

    os.system("cp ../runscript ./")
    os.system("qsub runscript")

    old_file.seek(0)

    os.chdir('../')

old_file.close()
new_file.close()
