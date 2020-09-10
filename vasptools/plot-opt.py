import numpy as np
import matplotlib.pyplot as plt

def get_tot_en() :
    """ get total energy from OSZICAR file
    """
    tot_ens = list()
    with open("OSZICAR", "r") as file :
        for line in file :
            if "E0" in line :
                tot_ens.append(float(line.split()[4]))
    return tot_ens

tot_ens = get_tot_en()
fig, axs = plt.subplots(ncols = 2)
axs[0].plot(np.arange(len(tot_ens)), tot_ens)
axs[1].plot(np.arange(1, len(tot_ens)), np.abs(np.diff(tot_ens)))
axs[0].set_xlabel("Step")
axs[1].set_xlabel("Step")
axs[0].set_ylabel("Total energy (eV)")
axs[1].set_ylabel("$\|E_{i}^{tot}-E_{i-1}^{tot}\|$")
axs[1].set_yscale("log")
fig.set_size_inches(8, 4)
plt.tight_layout()
plt.show()
