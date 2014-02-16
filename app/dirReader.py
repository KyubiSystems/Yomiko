#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import zipfile
import rarfile
import fnmatch
import hashlib
import split_tags as tag
from models import *

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


# Get MD5 checksum of input file
def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "r+b") as f:
        for block in iter(lambda: f.read(blocksize), ""):
            hash.update(block)
    return hash.hexdigest()


# Generate thumbnail and save to cache
def make_thumbnail(f):
    pass

# Find ZIPs and RARs in input directory
for f in os.listdir(INPUT_PATH):
    if fnmatch.fnmatch(f, '*.[Zz][Ii][Pp]'):
        zips.append(f)

    if fnmatch.fnmatch(f, '*.[Cc][Bb][Zz]'):
        zips.append(f)

    if fnmatch.fnmatch(f, '*.[Rr][Aa][Rr]'):
        rars.append(f)

    if fnmatch.fnmatch(f, '*.[Cc][Bb][Rr]'):
        rars.append(f)

# Loop over zips & rars, get tags from titles
# Add volume to DB
# Add tags to DB (many-to-many mapping)

# Scan individual ZIP file
for f in zips:
    print "Scanning ZIP: "+f,
    try:
        myzip = zipfile.ZipFile(INPUT_PATH+f, 'r')
    except zipfile.BadZipfile as e:
        raise Exception(u'"{}" is not a valid ZIP file! Error: {}'.format(f, e))
    except:
        raise Exception('Unknown error: {}, ZIP extraction failed: {}').format(e, f)

    zip_members = myzip.namelist()
    zip_members = filter(lambda x: is_image(x) is True, zip_members)
    zip_count = zip_members.count()
    print ' done.'
    print "Found {0} members.". format(str(zip_count))

    # Check if # images > 0
    if zip_count > 0:

        # Generate MD5 checksum for ZIP file
        md5 = md5sum(INPUT_PATH+f)

        # Add volume to DB Volume table
        vol = Volume.create(title=f, md5=md5, type='zip', num=zip_count, comments='')

        # Parse tags from filename, add to DB Tags table
        tags = tag.split_tags(f)
        for t in tags:
            # check if tag already exists, insert if not

            # insert tag and volume id into TagRelation table
            pass

        # Add pages to DB Image table
        page = 0
        for z in zip_members:
            im = Image.create(volume=vol.id, page=page, file=z)
            page += 1

        # Spawn greenlet processes to generate thumbnails
        # Display progress bars?

# Scan individual RAR file
for f in rars:
    print "Scanning RAR: "+f,
    try:
        myrar = rarfile.RarFile(INPUT_PATH+f, 'r')
    except (rarfile.BadRarFile, rarfile.NotRarFile) as e:
        raise Exception(u'"{}" is not a valid RAR file! Error: {}'.format(f, e))
    except:
        raise Exception("Unknown error: {}, RAR extraction failed: {}").format(e, f)

    rar_members = myrar.namelist()
    rar_members = filter(lambda x: is_image(x) is True, rar_members)
    rar_count = rar_members.count()
    print ' done.'
    print "Found {0} members.".format(str(rar_count))

    # Check if # images > 0
    if rar_count > 0:

        # Generate MD5 checksum for RAR file
        md5 = md5sum(INPUT_PATH+f)

        # Add volume to DB Volume table
        vol = Volume.create(title=f, md5=md5, type='rar', num=rar_count, comments='')

        # Parse tags from filename, add to DB Tags table
        tags = tag.split_tags(f)
        for t in tags:
            # check if tag already exists, insert if not

            # insert tag and volume id into TagRelation table
            pass

        # Add pages to DB Image table
        page = 0
        for r in rar_members:
            im = Image.create(volume=vol.id, page=page, file=r)
            page += 1

        # Spawn greenlet processes to generate thumbnails
        # Display progress bars?

