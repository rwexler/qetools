import os
import sys
import numpy as np
from numpy import linalg as LA

# remove gmon.out files produced by haise
os.system('find . -name "gmon.out" -delete')

##### settings #####

prefix = sys.argv[1] # get prefix for file names
h = 0.01*1.889725989 # displacement in bohr

##### function definitions #####

def getfolders(folders):
    os.system('ls -l > temp') # send list of file names to temp                                                                                                                                                  
    tempfile = open('temp', 'r') # read temp                                                                                                                                                                     
    next(tempfile) # skip line                                                                                                                                              
    for line in tempfile:
        if 'temp' in line:
            break
        list = line.split()
        folders.append(list[8]) # only grab file name                                                                                                                                                        
    tempfile.close()
    os.system('rm temp') # remove temp

def getforces(output,j,b):
    fxn = []; fyn = []; fzn = []
    for line in output: # find forces
        if 'Forces acting on atoms' in line:
            break
    next(output) # skip line
    for atom in range(nat):
        for line in output:
            list = line.split()
            fxn.append(float(list[6]))
            fyn.append(float(list[7]))
            fzn.append(float(list[8]))
            break
    if b == 0:
        return(fxn[j])
    elif b == 1:
        return(fyn[j])
    else:
        return(fzn[j])

def getmw(elm, mw):
    row = 0
    for i in range(nat):
        for a in range(3):
            row += 1 # set row index for hessian                                                                                                                                                                 
            col = 0
            for j in range(nat):
                for b in range(3):
                    col += 1 # set column index for hessian                                                                                                                                                    
                
                    # get mass 1                                                                                                                                                                                 
                    if elm[i] == 'H':
                        m1 = mH
                    elif elm[i] == 'O':
                        m1 = mO
                    elif elm[i] == 'P':
                        m1 = mP
                    elif elm[i] == 'Ni':
                        m1 = mNi
                    else:
                        print('error: element not yet implemented')

                    # get mass 2                                                                                                                                                                                
                    if elm[j] == 'H':
                        m2 = mH
                    elif elm[j] == 'O':
                        m2 = mO
                    elif elm[j] == 'P':
                        m2 = mP
                    elif elm[j] == 'Ni':
                        m2 = mNi
                    else:
                        print('error: element not yet implemented')
                
                    # construct mass weighting matrix                                                                                                                                                            
                    mw[row-1,col-1] = np.sqrt(m1*m2)

# get atom folder names
atomfolders = []
os.chdir('atoms')
getfolders(atomfolders)

# define direction folder names
dirfolders = ['x', 'y', 'z']

# get displacement folder names
dispfolders = []
os.chdir(atomfolders[0]+'/x/')
getfolders(dispfolders)
os.chdir('../../')

##### construct hessian #####
nat = len(atomfolders)

# initialize hessian
hessian = np.zeros(shape=(nat*3,nat*3))

# choose displaced atom
row = 0
for i in range(nat):

    # choose direction of displacement
    for a in range(3):
        row += 1 # set row index for hessian

        # choose responding atom
        col = 0
        for j in range(nat):
            
            # choose direction of response
            for b in range(3):
                col += 1 # set column index for hessian
                
                # enter folder for displaced atom
                os.chdir(atomfolders[i]+'/'+dirfolders[a])
                outputname = prefix+'.out'

                # get forces for negative displacement
                os.chdir(dispfolders[0])
                output = open(outputname, 'r')
                fneg = getforces(output,j,b)
                output.close()
                os.chdir('../')
                
                # get forces for positive displacement
                os.chdir(dispfolders[1])
                output = open(outputname, 'r')
                fpos = getforces(output,j,b)
                output.close()
                os.chdir('../')
                
                # calculate force constant using central difference
                k = (-1.*(fpos-fneg)/(2*h))
                k = k*778.4466886133225

                # construct hessian
                hessian[row-1,col-1] = k

                os.chdir('../../')
os.chdir('../')

##### generate mass weighted hessian #####

# get elements
elm = []
for i in range(nat):
    if 'Ni' in atomfolders[i]:
        elm.append(atomfolders[i][-2:])
    else:
        elm.append(atomfolders[i][-1:])

# get masses
mH = 1.00794*1.66054e-27 # kg
mO = 15.9994*1.66054e-27
mP = 30.973762*1.66054e-27
mNi = 58.6934*1.66054e-27

# generate mass weighting matrix
mw = np.zeros(shape=(nat*3,nat*3))
getmw(elm, mw)

# divide hessian by mw
mwhessian = np.divide(hessian, mw)

evals = np.sqrt(LA.svd(mwhessian)[1])/1e12/2/np.pi*33.35641
evalfile = open('evals.dat', 'w')
for i in range(len(evals)):
    evalfile.write(str(evals[i])+'\n')
evalfile.close()

# remove gmon.out files produced by haise
os.system('find . -name "gmon.out" -delete')
