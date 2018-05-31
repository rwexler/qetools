from glob import glob
import os

dirs = [dir for dir in glob("./*") if 'K' in dir]
for dir in dirs :
	os.chdir(dir)
	os.system("qsub runscript")
	os.chdir("../")
