import sys
from glob import glob
import os

filenames = sys.argv[1:]
for filename in filenames :
    os.system("unar -d {}".format(filename))
