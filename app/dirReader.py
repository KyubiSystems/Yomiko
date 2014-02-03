#!/usr/bin/env python

import zipfile
import rarfile
import os
import fnmatch
from config import *

zips = []
rars = []

# list of defined image extensions
IMAGE_EXTS = ['.gif', '.GIF', '.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']

# determine whether filename has image extension
def isImage(file):
    name, extension = os.path.splitext(file)
    if extension in IMAGE_EXTS:
        return True
    else:
        return False

for file in os.listdir(INPUT_PATH):
    if fnmatch.fnmatch(file, '*.[Zz][Ii][Pp]'):
        zips.append(file)

    if fnmatch.fnmatch(file, '*.[Rr][Aa][Rr]'):
        rars.append(file)

for file in zips:
    print "File: "+file
    myzip = zipfile.ZipFile(INPUT_PATH+file, 'r')
    zip_members = myzip.namelist()
    zip_members = filter(lambda x: isImage(x) is True, zip_members)
    print zip_members
    print '------------------'

for file in rars:
    print "File: "+file
    myrar = rarfile.RarFile(INPUT_PATH+file, 'r')
    rar_members = myrar.namelist()
    rar_members = filter(lambda x: isImage(x) is True, rar_members)
    print rar_members
    print '------------------'



