"""
Yomiko -- v0.02

(c) 2013 -- KyubiSystems

Web-based comics and doujinshi reader
Use SQLlite3 database for initial development and testing
"""

import zipfile
import rarfile
import sqlite3

from flask import Flask
app = Flask(__name__)

app.config.from_object('config')

print app.config['DATABASE_URI']

# CLASS DEFINITION ============================================

class Directory:
    """Directory(path) -- instantiate data directory object"""
    def __init__(self, Path):
        self.path = Path

    """scan() -- scans data directory for archive files"""
    def scan():
        pass

class Archive:
    """Archive() -- instantiate object for archive file"""
    def __init__():
        self.id=0
        self.type=""
        self.name=""
        self.size=0
        self.created=""
        self.path=""
        self.md5=""
        self.images=[]

    def getMetadata():
        pass

    def extractImage(n):
        pass

    def extractAll():
        pass

    def listImages():
        pass

    def clearCache():
        pass

class Image:
    """Image() -- instantiate object for individual image"""
    def __init__():
        self.archiveid=0
        self.imageid=0
        self.filename=""
        self.thumbnail=""
        self.cached=False

    def makeThumb():
        pass

    def getThumb():
        pass

    def showThumb():
        pass

    def getNext():
        pass

    def getPrev():
        pass

class Tagset:
    """Tagset() -- instantiate object for set of image tags"""
    self.archiveid=0
    self.tagid=0
    self.tag=""
    self.text=""

    def showTags():
        pass

    def addTag():
        pass

    def delTag():
        pass

# END CLASS DEFINITION ========================================   


