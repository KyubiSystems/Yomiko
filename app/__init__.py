"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from flask import Flask
from flask import g

# Import configuration
from config import *
from models import *

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
from views import *

