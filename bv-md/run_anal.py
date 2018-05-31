import os
import numpy as np

temp_dirs = ['020K', '030K', '040K', '050K', 
             '060K', '070K', '080K', '090K', '100K',
             '110K', '120K', '130K', '140K', '150K',
             '160K', '170K']
#temps = [185, 190, 195, 200]
#temp_dirs = [str(temp) + 'K' for temp in temps]

for temp in temp_dirs :
    os.chdir(temp)

    print 'running analysis for ' + temp
    #os.system('./batio3_anal_fast_lmp &')
    os.system('cp /p/home/rwexler/source/analyze/* ./')
    os.system('cp ../anal_run ./')
    os.system('qsub anal_run')

    os.chdir('../')
