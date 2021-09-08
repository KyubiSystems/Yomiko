#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2016 Kyubi Systems: www.kyubi.co.uk
"""

import fnmatch
import hashlib
import mimetypes
import os
import zipfile
import rarfile
from natsort import natsorted
from progressbar import Bar, ProgressBar, Counter, ETA

import app.tag_parse as tag
from app.config import INPUT_PATH, THUMB_PATH, DB_FILE
from app.models import Volume, Tag, TagRelation, Image, DoesNotExist
from app.db_utils import create_db
from app.image_utils import is_image, Page

zips = []
rars = []


# Get MD5 checksum of input file
def md5sum(filename, blocksize=65536):
    file_hash = hashlib.md5()
    with open(filename, "r+b") as f:
        for block in iter(lambda: f.read(blocksize), ""):
            file_hash.update(block)
    return file_hash.hexdigest()


def scan_archive_file(archives, filetype):
    # Loop over zips & rars, get tags from titles
    # Add volume to Volume DB
    # Add tags to Tag DB (many-to-many mapping)
    # Add pages to Image DB

    # initialise mimetypes
    mimetypes.init()

    # Iterate over input list of archive files
    for f in archives:

        # Attempt to scan ZIP file
        if filetype == 'zip':

            try:
                myfile = zipfile.ZipFile(INPUT_PATH+f, 'r')
            except zipfile.BadZipfile as e:
                raise Exception('"{}" is not a valid ZIP file! Error: {}'.format(f, e)) from e
            except:
                print('Unknown error: ZIP extraction failed: {}'.format(f))
                raise

        # Scan RAR file
        elif filetype == 'rar':

            try:
                myfile = rarfile.RarFile(INPUT_PATH+f, 'r')
            except (rarfile.BadRarFile, rarfile.NotRarFile) as e:
                raise Exception('"{}" is not a valid RAR file! Error: {}'.format(f, e)) from e
            except:
                print('Unknown error: RAR extraction failed: {}'.format(f))
                raise

        else:

            raise ValueError('Unrecognised archive type value: {}'.format(filetype))

        # Get members from archive
        members = myfile.namelist()

        # Filter member list for images
        members = [x for x in members if is_image(x) is True]

        # Sort members
        members = natsorted(members)

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
            disptitle = title[:20]
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

                # Guess mimetype for image from filename
                (mimetype, _) = mimetypes.guess_type(m)

                # Create record in Image table
                # >>> TODO: image record should include image height & width
                Image.create(volume=vol.id, page=page, mimetype=mimetype, filename=m)

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
    print("SQLite database not found, creating file " + DB_FILE + "...", end=' ')
    create_db()
    print("done.")

# Scan and process ZIP files
scan_archive_file(zips, 'zip')

# Scan and process RAR files
scan_archive_file(rars, 'rar')
