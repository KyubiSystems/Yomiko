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




