#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import zipfile
import rarfile
import fnmatch
from config import *

zips = []
rars = []

# list of defined image extensions
IMAGE_EXTS = ['.gif', '.GIF', '.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']


# determine whether filename has image extension
def is_image(f):
    name, extension = os.path.splitext(f)
    if extension in IMAGE_EXTS:
        return True
    else:
        return False

# Generate thumbnail and save to cache
def make_thumbnail(f):
    pass

# Find ZIPs and RARs in input directory
for f in os.listdir(INPUT_PATH):
    if fnmatch.fnmatch(f, '*.[Zz][Ii][Pp]'):
        zips.append(f)

    if fnmatch.fnmatch(f, '*.[Rr][Aa][Rr]'):
        rars.append(f)

# Loop over zips & rars, get tags from titles
# Add volume to DB
# Add tags to DB (many-to-many mapping)

# Scan individual ZIP file
for f in zips:
    print "Scanning ZIP: "+f,
    myzip = zipfile.ZipFile(INPUT_PATH+f, 'r')
    zip_members = myzip.namelist()
    zip_members = filter(lambda x: is_image(x) is True, zip_members)
    zip_count = zip_members.count()
    print ' done.'
    print "Found {0} members.". format(str(zip_count))

# Add ZIP members to DB

# Spawn greenlet processes to generate thumbnails

# Display progress bars?

# Scan individual RAR file
for f in rars:
    print "Scanning RAR: "+f,
    myrar = rarfile.RarFile(INPUT_PATH+f, 'r')
    rar_members = myrar.namelist()
    rar_members = filter(lambda x: is_image(x) is True, rar_members)
    rar_count = rar_members.count()
    print ' done.'
    print "Found {0} members.".format(str(rar_count))

# Add RAR members to DB

# Spawn greenlet processes to generate thumbnails

# Display progress bars?