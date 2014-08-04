#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

# Image handling utility
# Generates preview thumbnails

from PIL import Image, ImageFilter
from io import BytesIO
from os import rename, makedirs, path

import config

# Clean up class initialisation
# Better exception handling

# Assigns image binary object to Page class?
# Where's filename load method?
# Take binary directly from ZipFile output?
# Check for valid image data before write?
class Page(BytesIO):
    def get(self):
        return self.getvalue()

    def img(self):
        try:
            im = Image.open(BytesIO(self.get()))
            return im
        except:
            print "Unable to open image"

    def save(self, path):
        im = self.img()
        try:
            im.save(path, 'JPEG')
            return path
        except:
            print "Unable to save image"

    def size(self):
        return self.img().size

    def thumb(self, size=(THUMB_WIDTH, THUMB_HEIGHT)):
        im = self.img()
        try:
            im.thumbnail(size, Image.ANTIALIAS)
        except:
            print "Unable to create thumbnail"

        # How is thumbnail filename generated?
        self.seek(0)
        try:
            im.save(self, 'JPEG')
        except:
            print "Unable to save thumbnail"
