import os
import sys

##### settings #####

disp = [-0.01, 0.01] # set displacements
redHessian = True # construct a reduced Hessian (for surface adsorbates)
atomtodo = [0,8] # format is atom # minus 1, [0,8] does atoms 1 and 9
pseudodir = '~/pseudo' # set directory containing psps
os.chdir('relaxed')
prefix = sys.argv[1] # get prefix for file names
outputname = prefix+'.out'
output = open(outputname, 'r')
inputname = prefix+'.in'
input = open(inputname, 'r')
os.chdir('../')

##### define functions #####

def displace(i,a,d,xeq,yeq,zeq,xnew,ynew,znew):
    for j in range(len(xeq)):
        if j == i:
            if a == 0:
                xnew[j] = xeq[j] + d
                ynew[j] = yeq[j]
                znew[j] = zeq[j]
            elif a == 1:
                xnew[j] = xeq[j]
                ynew[j] = yeq[j] + d
                znew[j] = zeq[j]
            elif a == 2:
                xnew[j] = xeq[j]
                ynew[j] = yeq[j]
                znew[j] = zeq[j] + d
        else:
            xnew[j] = xeq[j]
            ynew[j] = yeq[j]
            znew[j] = zeq[j]

def inputgen(tempin,elm,xnew,ynew,znew):
    input.seek(0)
    newinputname = prefix+'.in'
    newinput = open(newinputname, 'w')

    for line in tempin:
        if 'calculation' in line:
            newinput.write('   calculation = "scf"\n')
            break
        newinput.write(line)

    for line in tempin:
        if 'pseudo_dir' in line:
            newinput.write('   pseudo_dir = "~/pseudo/"\n')
            break
        newinput.write(line)

    for line in tempin:
        if 'electron_maxstep' in line:
            newinput.write(line)
            break
        newinput.write(line)

    newinput.write('   startingpot = "file"\n')

    for line in tempin:
        if 'ATOMIC_POSITIONS' in line:
            newinput.write(line)
            break
        newinput.write(line)

    for i in range(nat):
        newinput.write(elm[i]+' '+str(xnew[i])+' '+str(ynew[i])+' '+str(znew[i])+'\n')
    newinput.close()

##### get information for calculation #####

# get the number of atoms
for line in output:
    if 'number of atoms' in line:
        list = line.split()
        nat = int(list[4])
        break
if (redHessian == True):
    nat = len(atomtodo)

# get the number of relaxation steps
nstep = 0
for line in output:
    if 'Forces acting on atoms' in line:
        nstep += 1
output.seek(0)

##### get the equilibrium forces #####

# find the final forces
temp = 0
for i in range(nstep):
    for line in output:
        if 'Forces acting on atoms' in line:
            temp += 1
            break
    if temp == nstep:
        break

# read the final forces
fxeq = []; fyeq = []; fzeq = []
next(output)
for i in range(nat):
    for line in output:
        list = line.split()
        fxeq.append(float(list[6]))
        fyeq.append(float(list[7]))
        fzeq.append(float(list[8]))
        break

##### get the final coordinates #####
elm = []; xeq = []; yeq = []; zeq = []
for line in output:
    if 'Begin final coordinates' in line:
        break
for i in range(2):
    next(output)
for i in range(nat):
    for line in output:
        list = line.split()
        elm.append(list[0])
        xeq.append(float(list[1]))
        yeq.append(float(list[2]))
        zeq.append(float(list[3]))
        break
output.close()

##### apply displacements and perform scf calculations
os.system('mkdir atoms')
os.chdir('atoms')
#for i in range(nat):
for i in atomtodo:

    # generate atom folder
    if i < 9:
        atomfolder = '0'+str(i+1)+'_'+elm[i]
    elif i >= 9 and i < 99:
        atomfolder = str(i+1)+'_'+elm[i]
    else:
        print('error: code cannot handle more than 100 atoms')
    os.system('mkdir '+atomfolder)
    os.chdir(atomfolder)

    for a in range(3):

        # generate direction folders
        if a == 0:
            dirfolder = 'x'
        elif a == 1:
            dirfolder = 'y'
        elif a == 2:
            dirfolder = 'z'
        else:
            print('error: cartesian direction not properly assigned')
        os.system('mkdir '+dirfolder)
        os.chdir(dirfolder)

        for k in range(len(disp)):

            # generate displacement folders
            if disp[k] < 0:
                dispfolder = 'n'+str(disp[k])[1:]
            else:
                dispfolder = 'p'+str(disp[k])
            os.system('mkdir '+dispfolder)
            os.chdir(dispfolder)

            # generate new coordinates
            xnew = [0]*nat; ynew = [0]*nat; znew = [0]*nat
            displace(i,a,disp[k],xeq,yeq,zeq,xnew,ynew,znew)

            # copy in environ file, runscript, and wave functions
            #os.system('cp ../../../../relaxed/environ.in ./')
            os.system('cp ../../../../relaxed/runscript ./')
            #os.system('cp -r ../../../../relaxed/*_*_mt.save ./')
            os.system('cp -r ../../../../relaxed/*.save ./')

            # generate input files
            inputgen(input,elm,xnew,ynew,znew)
            
            # run calculations
            os.system('qsub runscript')

            os.chdir('../')
        os.chdir('../')
    os.chdir('../')
os.chdir('../')
