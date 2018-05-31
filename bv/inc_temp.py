import sys

import os

# get old and new temperatures
old_temp = int(sys.argv[1])
new_temp = int(sys.argv[2])

# generate name of directory for new temperature
if new_temp < 100 :
    new_temp_dir = '../0' + str(new_temp) + 'K'
else :
    new_temp_dir = '../' + str(new_temp) + 'K'

# copy analysis functions
os.system('cp anal_fast_lmp.out batio3_anal_fast_lmp ' + new_temp_dir)

# generate name of old and new restart files
if old_temp < 100 :
    old_rest = 'BZTO.restart0' + str(old_temp)
else :
    old_rest = 'BZTO.restart' + str(old_temp)
if new_temp < 100 :
    new_rest = 'BZTO.restart0' + str(new_temp)
else :
    new_rest = 'BZTO.restart' + str(new_temp)

# copy restart file
os.system('cp ' + old_rest + ' ' + new_temp_dir)

# copy runscript
os.system('cp runscript ' + new_temp_dir)

# generate new input file
with open(new_temp_dir + '/in.BZTO', 'w') as new_f :
    with open('in.BZTO', 'r') as old_f :
        for line in old_f :
            if 'read_restart' in line :
                break
            else :
                new_f.write(line)
        new_f.write('read_restart ' + old_rest + '\n')
        for line in old_f :
            if 'fix 1' in line :
                break
            else :
                new_f.write(line)
        new_f.write('fix 1 all nvt temp ' + str(float(new_temp)) + ' ' + str(float(new_temp)) + ' 1.0\n')
        for line in old_f :
            if 'fix 2' in line :
                break
            else :
                new_f.write(line)
        new_f.write('fix 2 all npt temp ' + str(float(new_temp)) + ' ' + str(float(new_temp)) + ' 1.0 aniso 1.01325 1.01325 5.0\n')
        for line in old_f :
            if 'fix 3' in line :
                break
            else :
                new_f.write(line)
        new_f.write('fix 3 all npt temp ' + str(float(new_temp)) + ' ' + str(float(new_temp)) + ' 1.0 aniso 1.01325 1.01325 5.0\n')
        for line in old_f :
            if 'write_restart' in line :
                break
            else :
                new_f.write(line)
        new_f.write('write_restart ' + new_rest)

# submit lammps simulation at new temperature
os.chdir(new_temp_dir)
os.system('qsub runscript')
