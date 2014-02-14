"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""
import os

# set application path
APP_PATH = os.path.dirname(os.path.realpath(__file__))

# Set DEBUG to True for development
DEBUG = True

# Set SQLite3 database file path
DB_FILE = APP_PATH + '/db/Yomiko.db'

# Set input file path to scan for RAR/ZIP files
INPUT_PATH = os.path.expanduser('~/Downloads/')

# Set path for downloaded image cache
CACHE_PATH = APP_PATH + '/cache/'

# Set path for thumbnail store
THUMB_PATH = APP_PATH + '/thumbnails/'

# Set thumbnail default sizes
THUMB_WIDTH = 90
THUMB_HEIGHT = 125

# Set version string
APP_VERSION = 'YomikoCR/0.0.2'
