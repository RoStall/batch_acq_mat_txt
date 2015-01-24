__author__ = 'Robert Stallard '

"""

Batch *.acq data file conversion is performed here. Input directory and all *.acq files will be converted into *.txt and/or *.mat

This will create *.txt files from each *.acq in the directory -- including subdirectories??

"""
import bioread
import os
import glob
import h5py
import re

directory = raw_input('Input directory to convert here:')
# directory = 'E:\Dropbox\BedRestStudy\MVC_PRE_2-2'
dirfiles = os.listdir(directory)

# todo if user input lacks ending '\' add it.
if len(dirfiles) == 0:
    print "Specified directory is empty. press Enter to exit."
    os.system('pause')
    exit()

dirlen = len(dirfiles)


dir_list = []

file_list = glob.glob('*.acq') # get files with acq extension
for f in dirfiles:
    print f
    if os.path.isdir(directory + f) == True: # check if path is directory, make list of such
        dir_list.append(f)

for dir in dir_list:
    print dir
    file_list.extend(glob.glob(directory+'/'+dir+'/*.acq'))  # adding *.acq files from subdirectories to list

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

txtcount = 0
matcount = 0

for file in file_list:
    print file
    data = bioread.read_file(file)  # txtwriter writes channels selected from data (from bioread.read_file).
    base, ext = os.path.splitext(file)
    MatlabWriter.write_file(data, base + '.mat')  # write .mat
    matcount = matcount + 1
    dcnum = range(len(data.channels))  # TODO only works if sequential channels used

    for ch in dcnum:
        print data.channels[ch]
        channel_details = str(data.channels[ch])
        chname = re.search('Channel (.*):', channel_details)  # regex!
        basech = os.path.basename(file)  # Get name of file without directory structure
        path = os.path.dirname(file)  # Get path to file
        name, extension = os.path.splitext(basech)  # Split extension and filename
        savename = chname.group(1) + '.txt'  # the file's name itself -- no path

        # file names are that of the channel, so must be grouped in subdirectories.

        if not os.path.exists(path + '/' + name):
            os.makedirs(path +'/' + name)
        TxtWriter.write_file(data.channels[ch], path + '/' + name + '/' + savename)
        txtcount = txtcount + 1

print "Created %d *.mat files and %d *.txt files" % (matcount, txtcount)



# TxtWriter.write_file(data, "myfile.mat") # Creates a matlab file.
# TODO iterate through channels for each 'for file' and check that it isn't empty or out of list index range.
# TODO write each of these to text in own directory with same name as parent (e.g., datafile_txt) where directory and parent file are in same parent directory
# TODO get channel alias an put in as header.
# TODO eventually want single text file?
""" TxtWriter method contains some references to biopac.py via readers.py ? Needs further examination. May not be able to
simply alter that method to write channel data. """