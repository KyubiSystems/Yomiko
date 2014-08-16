#!/usr/bin/env python

import zipfile
import config
import os
from image_utils import Page, is_image

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

    p.thumb('./test/thumb_'+'{:03d}'.format(page)+'.jpg')

    print 'Thumbnail '+str(page)+' saved!'

    page += 1

fh.close()
