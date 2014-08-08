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

from config import *

# determine whether filename has image extension
def is_image(f):

# list of defined image extensions
    IMAGE_EXTS = ['.gif', '.GIF', '.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']

    name, extension = os.path.splitext(f)
    if extension in IMAGE_EXTS:
        return True
    else:
        return False

# Clean up class initialisation
# Better exception handling

# Assigns image binary object to Page class?
# Where's filename load method?
# Take binary directly from ZipFile output?
# Check for valid image data before write?
class Page(BytesIO):

    # Return binary object associated with Page
    def get(self):
        return self.getvalue()

    # Return binary object as Pillow image object
    def img(self):
        try:
            im = Image.open(BytesIO(self.get()))
            return im
        except:
            print "Unable to open image"

    # Save binary object to file as JPEG image
    # Check for directory existence at volume level?

    def save(self, filename):
        im = self.img()
        try:
            im.save(filename, 'JPEG')
            return filename
        except IOError:
            print "Unable to save image"

    # Return image size array
    def size(self):
        return self.img().size

    # Generate thumbnail from Page binary object 
    # set default size in config, can override
    # then save at path thumbname
    def thumb(self, thumbname, size=(THUMB_WIDTH, THUMB_HEIGHT)):
        im = self.img()
        try:
            im.thumbnail(size, Image.ANTIALIAS)
        except:
            print "Unable to create thumbnail"

        # im.save(outfile, format, options...)
        self.seek(0)
        try:
            im.save(thumbname, 'JPEG')
        except IOError:
            print "Unable to save thumbnail"
