#!/usr/bin/env python

import zipfile
import rarfile
import os
import fnmatch

from glob import glob as search


fileroot = '~/Downloads/'
fileroot = os.path.expanduser(fileroot)

zips = []
rars = []

for file in os.listdir(fileroot):
    if fnmatch.fnmatch(file, '*.[Zz][Ii][Pp]'):
        zips.append(file)

    if fnmatch.fnmatch(file, '*.[Rr][Aa][Rr]'):
        rars.append(file)

for file in zips:
    print "File: "+file
    myzip = zipfile.ZipFile(fileroot+file,'r')
    zip_members = myzip.namelist()
    print zip_members
    print '------------------'

for file in rars:
    print "File: "+file
    myrar = rarfile.RarFile(fileroot+file,'r')
    rar_members = myrar.namelist()
    print rar_members
    print '------------------'

