""" Program for performing VASP k-point convergence tests """

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'

import os
import subprocess
import sys
from shutil import copyfile


def main(nk_min, nk_max, nk_stp):
    """
Main program
    """
    cwd = os.getcwd()
    fname_old = os.path.abspath("KPOINTS")
    for nk in range(nk_min, nk_max + nk_stp, nk_stp):
        dname = "{:02d}".format(nk)
        if not os.path.exists(dname):
            os.makedirs(dname)
        copyfile("INCAR", dname)
        copyfile("POSCAR", dname)
        copyfile("POTCAR", dname)
        copyfile("runscript", dname)
        os.chdir(dname)
        with open("KPOINTS", "w") as f_new:
            with open(fname_old) as f_old:
                for i in range(3):
                    for line in f_old:
                        f_new.write(line)
                        break
                f_new.write("{0:3d} {0:2d} {0:2d}".format(nk))
                next(f_old)
                for line in f_old:
                    f_new.write(line)
        subprocess.run(["qsub", "runscript"])
        os.chdir(cwd)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
