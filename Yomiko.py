#!/usr/bin/env python

# Web-based comics & doujinshi reader
# Use SQLite3 database for initial development and testing

import zipfile
import rarfile
import sqllite3

from datetime import datetime
from file_utils import readConfig
from string import Template

# read config file

Config = readConfig('config.json')

# Print Content-Type: header + blank line
print "Content-Type: text/html"
print 
