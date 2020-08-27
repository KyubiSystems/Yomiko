"""
Yomiko Comics Reader
(c) 2016 Kyubi Systems: www.kyubi.co.uk
"""

from flask import Flask, g

# Set path for local imports
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname("__file__"), '..')))

# Import configuration
from app.config import APP_PATH, APP_VERSION, DB_FILE, DEBUG, INPUT_PATH, THUMB_HEIGHT, THUMB_PATH, THUMB_WIDTH
from app.models import *

app = Flask(__name__)

database = SqliteDatabase(DB_FILE)

# Request handlers provided by Flask
# Used to create and tear down a database connection
# on each request

@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

# Import views
from app.views import *

