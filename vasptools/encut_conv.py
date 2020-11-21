""" Program for performing VASP ENCUT convergence tests """

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'

import os
import subprocess
import sys
from shutil import copyfile


def main(ec_min, ec_max, ec_stp):
    """
Main program
    """
    cwd = os.getcwd()
    fname_old = os.path.abspath("INCAR")
    for ec in range(ec_min, ec_max + ec_stp, ec_stp):
        dname = str(ec)
        if not os.path.exists(dname):
            os.makedirs(dname)
        copyfile("KPOINTS", dname + "/KPOINTS")
        copyfile("POSCAR", dname + "/POSCAR")
        copyfile("POTCAR", dname + "/POTCAR")
        copyfile("runscript", dname + "/runscript")
        os.chdir(dname)
        with open("INCAR", "w") as f_new:
            with open(fname_old) as f_old:
                for line in f_old:
                    if "ENCUT" in line:
                        f_new.write("ENCUT = " + dname + "\n")
                    else:
                        f_new.write(line)
        subprocess.run(["qsub", "runscript"])
        os.chdir(cwd)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
