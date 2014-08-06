#!/usr/bin/env python

import zipfile
import config
from image_utils import Page

fh = open('test/input.zip', 'rb')

z = zipfile.ZipFile(fh)

foo = z.read('Done/009.png')

p = Page(foo)

print p.size()

p.thumb('./test/thumb.jpg')

print 'Thumbnail saved!'

fh.close()
