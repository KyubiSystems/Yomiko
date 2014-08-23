#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import zipfile
import rarfile
import fnmatch
import hashlib
import os

import tag_parse as tag
from models import *
from db_utils import create_db
from image_utils import is_image, Page
from progressbar import Bar, ProgressBar, Counter, ETA

zips = []
rars = []


# Get MD5 checksum of input file
def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "r+b") as f:
        for block in iter(lambda: f.read(blocksize), ""):
            hash.update(block)
    return hash.hexdigest()


def scan_archive_file(archives, filetype):
    # Loop over zips & rars, get tags from titles
    # Add volume to Volume DB
    # Add tags to Tag DB (many-to-many mapping)
    # Add pages to Image DB

    # Iterate over input list of archive files
    for f in archives:

        # Attempt to scan ZIP file        
        if filetype == 'zip':

            try:
                myfile = zipfile.Zipfile(INPUT_PATH+f, 'r')
            except zipfile.BadZipfile as e:
                raise Exception(u'"{}" is not a valid ZIP file! Error: {}'.format(f, e))
            except:
                print u'Unknown error: ZIP extraction failed: {}'.format(f)
                raise

        # Scan RAR file
        elif filetype == 'rar':

            try:
                myfile = rarfile.RarFile(INPUT_PATH+f, 'r')
            except (rarfile.BadRarFile, rarfile.NotRarFile) as e:
                raise Exception(u'"{}" is not a valid RAR file! Error: {}'.format(f, e))
            except:
                print u'Unknown error: RAR extraction failed: {}'.format(f)
                raise

        else:
        
            raise ValueError("Unrecognised archive type value: {}").format(filetype)

        # Get members from archive
        members = myfile.namelist()

        # Filter member list for images
        members = filter(lambda x: is_image(x) is True, members)
        
        # Get number of images
        member_count = len(members)

        # If images found...
        if member_count > 0:

            # Generate MD5 checksum for archive file
            md5 = md5sum(INPUT_PATH+f)

            # Parse title, tags from filename
            title, tags = tag.split_title_tags(f)

            # Add volume to DB Volume table
            vol = Volume.create(title=title, filename=f, md5=md5, filetype=filetype, num=member_count, comments='')

            # Add tags to DB Tags table
            for t in tags:
                # check if tag already exists, insert if not
                try:
                    new_tag = Tag.get(Tag.name == t)
                except DoesNotExist:
                    new_tag = Tag.create(name=t, descr='')

                # insert tag and volume id into TagRelation table
                TagRelation.create(relVolume=vol.id, relTag=new_tag.id)

            # Reset page counter (assume cover is page 0)
            page = 0  

            # Generate display title
            disptitle=title[:20]
            if len(disptitle) < len(title):
                disptitle = disptitle+'...'
            disptitle.ljust(24)

            # initialise progress bar display
            widgets = [disptitle+': ', Counter(),'/'+str(member_count)+' ', Bar(marker='=', left='[', right=']'), ETA()]
            pbar = ProgressBar(widgets=widgets, maxval=member_count).start()
            
            # Attempt to create thumbnail directory if it doesn't already exist
            path = THUMB_PATH + str(vol.id)

            try:
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise

            # Iterate over images in zip file
            for m in members:

                # Create record in Image table
                # >>> TODO: image record should include image height & width
                im = Image.create(volume=vol.id, page=page, filename=m)

                # Generate thumbnails
                # >>> TODO: May spawn greenlets to do this?

                # Read data from archive
                rawdata = myfile.read(m)
                
                # Generate Page object
                p = Page(rawdata)

                # Create thumbnail
                p.thumb(path+'/'+'{:03d}'.format(page)+'.jpg')
                
                # Update progress bar
                pbar.update(page)
                page += 1

            
            # end progress bar
            pbar.finish()

        # Close archive
        myfile.close()

        

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

# Check for existence of SQLite3 database, creating if necessary
if not os.path.exists(DB_FILE):
    print "SQLite database not found, creating file " + DB_FILE + "...",
    create_db()
    print "done."

# Scan and process ZIP files
scan_archive_file(zips, 'zip')

# Scan and process RAR files
scan_archive_file(rars, 'rar')
