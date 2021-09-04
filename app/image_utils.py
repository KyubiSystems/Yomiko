#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2016 Kyubi Systems: www.kyubi.co.uk
"""

# Image handling utility
# Generates preview thumbnails

import os
from io import BytesIO
from PIL import Image

from .config import THUMB_WIDTH, THUMB_HEIGHT

# determine whether filename has image extension
def is_image(f):

# list of defined image extensions
    IMAGE_EXTS = ['.gif', '.GIF', '.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']

    _, extension = os.path.splitext(f)
    if extension in IMAGE_EXTS:
        return True

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
            print("Unable to open image") # TODO: handle missing image exception

    # Save binary object to file as JPEG image
    # Check for directory existence at volume level?

    def save(self, filename):
        im = self.img()
        try:
            im.convert('RGB').save(filename, 'JPEG', quality=90)
            return filename
        except IOError:
            print("Unable to save image")
            raise

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
            print("Unable to create thumbnail")
            raise

        # im.save(outfile, format, options...)
        self.seek(0)
        try:
            im.convert('RGB').save(thumbname, 'JPEG', quality=90)
        except IOError:
            print("Unable to save thumbnail")
            raise
