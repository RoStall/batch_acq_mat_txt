__author__ = 'Robert Stallard '

"""

Batch *.acq data file conversion is performed here. Input directory and all *.acq files will be converted into *.txt and/or *.mat

This will create *.txt files from each *.acq in the directory -- including subdirectories??

"""
import bioread
import os
import glob
import h5py

#directory = raw_input('Input directory to convert here:')
directory = 'E:\Dropbox\BedRestStudy\MVC_PRE_2-2_test'
dirfiles = os.listdir(directory)

# todo if user input contains \ already after end of directory, remove it.
if len(dirfiles) == 0:
    print "Specified directory is empty. press Enter to exit."
    os.system('pause')
    exit()

dirlen = len(dirfiles)


dir_list = []

file_list = glob.glob('*.acq')
for f in dirfiles:
    print f
    if os.path.isdir('E:/Dropbox/BedRestStudy/MVC_PRE_2-2_test/'+f) == True:
        dir_list.append(f)

for dir in dir_list:
    print dir
    file_list.extend(glob.glob(directory+'/'+dir+'/*.acq'))

print file_list
print dir_list

"""
 TODO want list of directories terminating with filename, ultimately. Then iterate over them. Do not recurse into further
 subdirectories. Encourage flat organization of studies rather than nested subdirectories. Place converted files in same
 directory as originals.

 E.G., \organizingdirectory
            \study number 1
                \*.acq
                    .
                    .
            \study number n
                \*.acq
"""
from bioread.writers import TxtWriter
from bioread.writers import MatlabWriter

# Check # of data channels



for file in file_list:
    print file
    data = bioread.read_file(file) # txtwriter seems to write channels selected from data (from bioread.read_file).
    base, ext = os.path.splitext(file)
    MatlabWriter.write_file(data, base + '.mat')  # write .mat
    dcnum = range(len(data.channels)) # TODO only works if sequential channels used
    for ch in dcnum:
        print data.channels[ch]
        base = os.path.basename(file)  # Get name of file without directory structure
        path = os.path.dirname(file)  # Get path to file
        name, extension = os.path.splitext(base)  # Split extension and filename
        savename = name + 'ch_' + str(ch) + '.txt'  # the file's name itself -- no path
        TxtWriter.write_file(data.channels[ch], path + '/' + name + '/' + savename)




# TxtWriter.write_file(data, "myfile.mat") # Creates a matlab file.
# TODO iterate through channels for each 'for file' and check that it isn't empty or out of list index range.
# TODO write each of these to text in own directory with same name as parent (e.g., datafile_txt) where directory and parent file are in same parent directory
# 