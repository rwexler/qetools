import numpy as np
import sys

# read data file #--------------------------------------------------
data_file_name = sys.argv[1]

# get number of atoms
with open(data_file_name, 'r') as data_file :
    for line in data_file :
        if 'atoms' in line :
            nat = int(line.split()[0])
            break

# get charges, molecules,  and atom coordinates
molecules = np.zeros((nat, ))
charges = np.zeros((nat, ))
at_coord = np.zeros((nat, 3))
with open(data_file_name, 'r') as data_file :
    for line in data_file :
        if 'Atoms' in line :
            break
    for line in data_file :
        break
    for i in range(nat) :
        for line in data_file :
            molecules[i] = int(line.split()[1])
            charges[i] = float(line.split()[3])
            at_coord[i, :] = np.array(line.split()[4:7]).astype(float)
            break

# get number of molecules and waters
nmol = int(molecules[-1] / 2.)

# read dump file #--------------------------------------------------
dump_file_name = sys.argv[2]

# get number of trajectories
ntraj = 0
with open(dump_file_name, 'r') as dump_file :
    for line in dump_file :
        if 'ITEM: TIMESTEP' in line :
            ntraj += 1

# calculate ionic polarization for each structure
dip_mom_all = []
dip_mom_all_molecule = []
dip_mom_all_water = []
with open(dump_file_name, 'r') as dump_file :
    for i in range(ntraj) :
        print i + 1, ' traj of ', ntraj

        # get lattice constants
        for line in dump_file :
            if 'ITEM: BOX BOUNDS' in line :
                break
        lat_cst = np.zeros((3, ))
        for j in range(3) :
            for line in dump_file :
                min = float(line.split()[0])
                max = float(line.split()[1])
                lat_cst[j] = max - min
                break

        # calculate dipole moment
        for line in dump_file :
            if 'ITEM: ATOMS' in line :
                break
        dip_mom_x = 0
        dip_mom_y = 0
        dip_mom_z = 0
        dip_mom_x_molecule = 0
        dip_mom_y_molecule = 0
        dip_mom_z_molecule = 0
        dip_mom_x_water = 0
        dip_mom_y_water = 0
        dip_mom_z_water = 0
        for j in range(nat) :
            for line in dump_file :
                xi = at_coord[j, 0]
                yi = at_coord[j, 1]
                zi = at_coord[j, 2]
                xf = float(line.split()[2])
                yf = float(line.split()[3])
                zf = float(line.split()[4])
                dx = xf - xi
                dy = yf - yi
                dz = zf - zi

                # use pbs to move atom near original coordinate
                if (xf - xi < lat_cst[0] * 0.5) :
                    xf += lat_cst[0]
                if (xf - xi > lat_cst[0] * 0.5) :
                    xf -= lat_cst[0]
                if (yf - yi < lat_cst[1] * 0.5) :
                    yf += lat_cst[1]
                if (yf - yi > lat_cst[1] * 0.5) :
                    yf -= lat_cst[1]
                if (zf - zi < lat_cst[2] * 0.5) :
                    zf += lat_cst[2]
                if (zf - zi > lat_cst[2] * 0.5) :
                    zf -= lat_cst[2]
                
                # calculate x, y, and z-components of dipole moment
                dip_mom_x += xf * charges[j]
                dip_mom_y += yf * charges[j]
                dip_mom_z += zf * charges[j]
                if molecules[j] <= nmol :
                    dip_mom_x_molecule += xf * charges[j]
                    dip_mom_y_molecule += yf * charges[j]
                    dip_mom_z_molecule += zf * charges[j]
                else :
                    dip_mom_x_water += xf * charges[j]
                    dip_mom_y_water += yf * charges[j]
                    dip_mom_z_water += zf * charges[j]
                break

        dip_mom_all.append([dip_mom_x, dip_mom_y, dip_mom_z])
        dip_mom_all_molecule.append([dip_mom_x_molecule,
                                     dip_mom_y_molecule,
                                     dip_mom_z_molecule])
        dip_mom_all_water.append([dip_mom_x_water,
                                  dip_mom_y_water,
                                  dip_mom_z_water])

# save dipole moments as csv file
dip_mom_all = np.array(dip_mom_all)
dip_mom_all_molecule = np.array(dip_mom_all_molecule)
dip_mom_all_water = np.array(dip_mom_all_water)
np.savetxt('dip_mom_all.csv', dip_mom_all, delimiter=',')
np.savetxt('dip_mom_all_molecule.csv', dip_mom_all_molecule, delimiter=',')
np.savetxt('dip_mom_all_water.csv', dip_mom_all_water, delimiter=',')
