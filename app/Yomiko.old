#!/usr/bin/env python

"""
Yomiko -- v0.01

(c) 2013 -- KyubiSystems

Web-based comics & doujinshi reader
Use SQLite3 database for initial development and testing
"""

import zipfile
import rarfile
import sqlite3

from datetime import datetime
from file_utils import readConfig
from string import Template

# read config file

Config = readConfig('config.json')

# initialise path configuration

filePath = Config['filePath']
cachePath = Config['cachePath']

# Print Content-Type: header + blank line
print "Content-Type: text/html"
print 

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

    
