"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import os
import zipfile
import fnmatch
from config import *
from flask import Flask, render_template, send_file
from io import BytesIO
from image_utils import is_image

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/list')
def plist():
    return render_template("list.html")

@app.route('/tags')
def tags():
    return render_template("tags.html")

# Application settings

@app.route('/settings')
def settings():
    return render_template("settings.html")

# Render title (grid of thumbnails). Cover?

@app.route('/title/<int:title_id>')
def title(title_id):

    # TEST: for testing purposes set title_id =0
    title_id = 0

    # Get list of thumbnails for this title
    # replace directory glob with DB query?
    thumbs = []
    for f in os.listdir(APP_PATH+ '/static/thumbnails/'+str(title_id)):
        if fnmatch.fnmatch(f,'*thumb.jpg'):
            thumbs.append(f)

    # extend to returning dictionary of page number, thumbnail URL
    # iterate in page number
    
    # pass list of thumbnails to template
    return render_template("title.html",name='testing',id=str(title_id),thumbs=thumbs)

# Render individual page image

@app.route('/page/<int:title_id>/<int:page_num>')
def page(title_id, page_num):

    # DB query to get archive file corresponding to title ID
    # abstract to volume class?

    fh = open(APP_PATH+'/test/input.zip', 'rb')

    z = zipfile.ZipFile(fh)

    # Get members from archive
    members = z.namelist()

    # Filter member list for images
    members = filter(lambda x: is_image(x) is True, members)

    # Get number of members
    member_count = len(members)

    if page_num < member_count:

        foo = z.read(members[page_num])

        mimetype = 'image/jpeg'

        fh.close()

        # return extracted image to browser
        return send_file(BytesIO(foo), mimetype=mimetype)

    else: 

        fh.close()
        
        abort(404)

# Test page

@app.route('/hello')
def hello_world():
    return 'Hello world!'

# Error handling

@app.errorhandler(404)
def internal_error(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(errror):
    db.session.rollback()
    return render_template("500.html"), 500

