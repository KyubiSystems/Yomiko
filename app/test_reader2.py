#!/usr/bin/env python

import zipfile
import config
import os
from image_utils import Page


# list of defined image extensions
IMAGE_EXTS = ['.gif', '.GIF', '.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']


# determine whether filename has image extension
def is_image(f):
    name, extension = os.path.splitext(f)
    if extension in IMAGE_EXTS:
        return True
    else:
        return False


fh = open('test/input.zip', 'rb')

try:
    z = zipfile.ZipFile(fh)
except zipfile.BadZipfile as e:
    raise Exception(u'"{}" is not a valid ZIP file! Error: {}'.format(z, e))
except:
    print u'Unknown error: ZIP extraction failed: {}'.format(z)
    raise

# Get members from archive
members = z.namelist()

# Filter member list for images
members = filter(lambda x: is_image(x) is True, members)

# Get number of members
member_count = len(members)

page = 0

# Iterate over ZIP members, generate thumbnails
for m in members:
    
    foo = z.read(m)

    p = Page(foo)

    p.thumb('./test/'+str(page)+'_thumb.jpg')

    print 'Thumbnail '+str(page)+' saved!'

    page += 1

fh.close()
