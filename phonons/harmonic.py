import sys
import numpy as np
import os

filename = sys.argv[1]

freqs = np.array(os.popen("grep freq dynmat.out | cut -f 3 -d = | cut -f 1 -d [").read().split()).astype(float)

def calc_zpe(freqs) :
    """calculate the zero point energy
    """
    wn_per_ev = 8065.54429
    return np.sum(freqs[3:]) / 2. / wn_per_ev

def calc_fvib_temp(freqs, temp) :
    """calculate the helmholtz free energy at a specific temperature
    """
    k = 8.6173303e-5
    wn_per_ev = 8065.54429
    zpe = calc_zpe(freqs)
    return zpe + k * temp * np.sum(np.log(1 - np.exp(-freqs[3:] / k / temp / wn_per_ev)))

def calc_fvib(freqs) :
    """calculate the helmholtz free energy for a range of temperatures
    """
    temps = np.arange(1, 501, 1)
    fvibs = list()
    for temp in temps :
        fvibs.append(calc_fvib_temp(freqs, temp))
    fvibs = np.array(fvibs)
    return np.vstack((temps, fvibs)).T

fvibs = calc_fvib(freqs)
np.savetxt("fvibs.csv", fvibs, delimiter = ",")
