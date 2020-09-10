import sys
import os
import numpy as np
import csv

filename = sys.argv[1]

nat = int(os.popen("grep 'Atom #' "+filename+" | cut -f 1 -d ':' | cut -f 2 -d '#' | tail -1").read())
charges = np.array(os.popen("grep 'Atom #' "+filename).read().split("\n"))[:-1].reshape((nat, 3))

def tidyproj(projs) :
    """tidy up charge projections"""
    dict = {}
    for i, proj in enumerate(projs) :
        if i == 0 :
            dict["total"] = float(proj.split()[6][:-1])
            dict["s"] = float(proj.split()[9][:-1])
        elif i == 1 :
            dict["p"] = float(proj.split()[9][:-1])
            dict["pz"] = float(proj.split()[11][:-1])
            dict["px"] = float(proj.split()[13][:-1])
            dict["py"] = float(proj.split()[15][:-1])
        else :
            dict["d"] = float(proj.split()[9][:-1])
            dict["dz2"] = float(proj.split()[11][:-1])
            dict["dxz"] = float(proj.split()[13][:-1])
            dict["dyz"] = float(proj.split()[15][:-1])
            dict["dx2-y2"] = float(proj.split()[17][:-1])
            dict["dxy"] = float(proj.split()[19][:-1])
    return dict

toCSV = list()
for i, charge in enumerate(charges) :
    toCSV.append(tidyproj(charge))

# convert to csv
# https://stackoverflow.com/questions/3086973/how-do-i-convert-this-list-of-dictionaries-to-a-csv-file
keys = toCSV[0].keys()
with open('lowdin.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writer.writerow(keys)
    dict_writer.writerows(toCSV)
