""" Program for performing VASP atom box convergence tests """

__author__ = 'Robert B. Wexler'
__email__ = 'robertowexler@gmail.com'

import os
import subprocess
import sys
from shutil import copyfile


def main(a_min, a_max, a_stp):
    """
Main program
    """
    cwd = os.getcwd()
    fname_old = os.path.abspath("POSCAR")
    for a in range(a_min, a_max + a_stp, a_stp):
        dname = "{:02d}".format(a)
        if not os.path.exists(dname):
            os.makedirs(dname)
        copyfile("INCAR", dname + "/INCAR")
        copyfile("KPOINTS", dname + "/KPOINTS")
        copyfile("POTCAR", dname + "/POTCAR")
        copyfile("runscript", dname + "/runscript")
        os.chdir(dname)
        with open("POSCAR", "w") as f_new:
            with open(fname_old) as f_old:
                for i in range(2):
                    for line in f_old:
                        f_new.write(line)
                        break
                f_new.write("{} 0 0\n".format(a))
                f_new.write("0 {} 0\n".format(a + 0.5))
                f_new.write("0 0 {}\n".format(a + 1))
                for i in range(3):
                    for line in f_old:
                        break
                for line in f_old:
                    f_new.write(line)
        subprocess.run(["qsub", "runscript"])
        os.chdir(cwd)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
