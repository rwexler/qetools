import sys
import numpy as np
import os

# how to run
# python submit_jobs_on_hold.py runscript 10sr

batch_script_filename = sys.argv[1]
batch_script_old = open(batch_script_filename, 'r')
temperatures = np.arange(20, 180, 10).tolist()
dopant_concentration = str(sys.argv[2])

for temperature in temperatures :

    if temperature < 100 :
        directory = '0' + str(temperature) + 'K'
    else :
        directory = str(temperature) + 'K'

    os.chdir(directory)
    
    with open(batch_script_filename, 'w') as batch_script_new :
        for line in batch_script_old :
            if '-N' in line :
                batch_script_new.write('#PBS -N ' + dopant_concentration + '_' + 
                                       directory + '\n')
            else :
                batch_script_new.write(line)
    batch_script_old.seek(0)

    os.system('qsub runscript > temp')

    with open('temp', 'r') as temp :
        for line in temp :
            job_id = line.split('.')[0]
            break

    os.system('qhold ' + job_id)

    os.chdir('../')

batch_script_old.close()
