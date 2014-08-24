"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import os
import zipfile
import fnmatch
import mimetypes
from config import *
from flask import Flask, abort, render_template, send_file
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

    # DB query to Get tag information
    # TODO: Need to get tag count by join...
    tags = Tag.select()

    return render_template("tags.html", tags=tags)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):

    # DB query to get specific tag
    try:
        tag = Tag.get(id == tag_id)
    except Tag.DoesNotExist:
        abort(404)

    return render_template("tags.html", tags=tag)

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):

    # DB query to get specific tag
    try:
        tag = Tag.get(id == tag_id)
    except Tag.DoesNotExist:
        abort(404)

    return render_template("tags.html", tags=tag)

# Filter operations

@app.route('/filter/<filter_string>')
def filter_tags(filter_string):

    # filter string is dot-separated list of tag IDs

    # TODO: Check how to do filter search on titles

    return render_template("tags.html")

# Application settings

@app.route('/settings')
def settings():
    return render_template("settings.html")

# Render title (grid of thumbnails).
# Image 0 as blurred CSS background?

@app.route('/title/<int:title_id>')
def title(title_id):

    # Get title information
    try:
        volume = Volume.get(id == title_id)
    except Volume.DoesNotExist:
        abort(404)

    # Get list of images for this title
    thumbs = Image.select().where(volume_id == title_id).order_by(Image.page)
    
    # pass list of thumbnails to template
    return render_template("title.html",title=volume.title,id=str(title_id),thumbs=thumbs)

# Render individual page image

@app.route('/page/<int:title_id>/<int:page_num>')
def page(title_id, page_num):

    # Initialise mimetypes
    mimetypes.init()

    # DB query to get archive file corresponding to title ID
    # and member file corresponding to page number

    # Get title information
    try:
        volume = Volume.get(id == title_id)
    except Volume.DoesNotExist:
        abort(404)

    # Get page information
    try:
        page = Image.get((volume_id == title_id) & (page == page_num))
    except Image.DoesNotExist:
        abort(404)

    # open archive file
    # TODO: Error checking
    fh = open(INPUT_PATH+volume.filename, 'rb')
    z = zipfile.ZipFile(fh)

    # Get page binary data
    # TODO: Error checking
    foo = z.read(page.filename)

    fh.close()

    # Return extracted image to browser
    return send_file(BytesIO(foo), mimetype=page.mimetype)

# Error handling

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(errror):
    db.session.rollback()
    return render_template("500.html"), 500

