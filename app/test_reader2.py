#!/usr/bin/env python

import zipfile
import config
import os
from image_utils import Page, is_image
from progressbar import Bar, ProgressBar, Counter, ETA

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

print 'Starting...'

# initialise progress bar display
widgets = ['Title: ', Counter(),'/'+str(member_count)+' ', Bar(marker='=', left='[', right=']'), ETA()]
pbar = ProgressBar(widgets=widgets, maxval=member_count).start()

# Iterate over ZIP members, generate thumbnails
for m in members:
    
    foo = z.read(m)

    p = Page(foo)

    p.thumb('./test/thumb_'+'{:03d}'.format(page)+'.jpg')

#    print 'Thumbnail '+str(page)+' saved!'

    pbar.update(page)
    page += 1

pbar.finish()
fh.close()

print 'Done!'
