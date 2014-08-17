"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import os
import zipfile
import fnmatch
import mimetypes
from config import *
from flask import Flask, render_template, send_file
from io import BytesIO
from image_utils import is_image


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# List of titles

@app.route('/list')
def plist():
    return render_template("list.html")

# Tag operations

@app.route('/tags')
def tags():
    return render_template("tags.html")

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    return render_template("tags.html")

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    return render_template("tags.html")

# Filter operations

@app.route('/filter/<filter_string>')
def filter_tags(filter_string):
    return render_template("tags.html")

# Application settings

@app.route('/settings')
def settings():
    return render_template("settings.html")

# Render title (grid of thumbnails).
# Image 0 as blurred CSS background?

@app.route('/title/<int:title_id>')
def title(title_id):

    # TEST: for testing purposes set title_id =0
    title_id = 0

    # Get list of thumbnails for this title
    # replace directory glob with DB query
    thumbs = []
    page = 0
    for f in os.listdir(APP_PATH+ '/static/thumbnails/'+str(title_id)):
        if fnmatch.fnmatch(f,'thumb*.jpg'):
            thumbs.append({'page': page, 'path': f})
            page += 1

    # extend to returning dictionary of page number, thumbnail URL
    # iterate in page number
    
    # pass list of thumbnails to template
    return render_template("title.html",title='testing',id=str(title_id),thumbs=thumbs)

# Render individual page image

@app.route('/page/<int:title_id>/<int:page_num>')
def page(title_id, page_num):

    # Initialise mimetypes
    mimetypes.init()

    # DB query to get archive file corresponding to title ID
    # and member file corresponding to page number

    # abstract to volume class?

    # TEST INPUT FILE
    fh = open(APP_PATH+'/test/input.zip', 'rb')

    z = zipfile.ZipFile(fh)

    # Get members from archive
    members = z.namelist()

    # Filter member list for images
    # This should already be done on import
    members = filter(lambda x: is_image(x) is True, members)

    # Get number of members
    member_count = len(members)

    if page_num < member_count:

        # Guess mimetype for image from filename
        (mimetype, encoding) = mimetypes.guess_type(members[page_num])

        foo = z.read(members[page_num])

        fh.close()

        # return extracted image to browser
        return send_file(BytesIO(foo), mimetype=mimetype)

    else: 

        fh.close()
        
        abort(404)

# Error handling

@app.errorhandler(404)
def internal_error(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(errror):
    db.session.rollback()
    return render_template("500.html"), 500

