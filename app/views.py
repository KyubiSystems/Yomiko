"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

import os
import zipfile
import rarfile
import fnmatch
from config import *
from flask import Flask, abort, render_template, send_file
from models import *
from io import BytesIO
from image_utils import is_image


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# List of titles

@app.route('/view/list')
def plist():

    vols = Volume.select().order_by(Volume.title)

    return render_template("list.html", vols=vols)


@app.route('/view/thumbs')
def tlist():

    vols = Volume.select().order_by(Volume.title)

    return render_template("thumbs.html", vols=vols)

# ---- Tag operations -----

# Show all tags
@app.route('/tags')
def alltags():

    tags = Tag.select().order_by(Tag.name)

    return render_template("tags.html", tags=tags)

# Show titles associated with given tag
@app.route('/tags/<int:tag_id>')
def showtag():

    try:
        tags = Tag.select().where(Tag.id == tag_id).order_by(Tag.name)
    except Tag.DoesNotExist:
        abort(404)

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
        volume = Volume.get(Volume.id == title_id)
    except Volume.DoesNotExist:
        abort(404)

    # Get list of images for this title
    thumbs = Image.select(Image,Volume).join(Volume).where(Volume.id == title_id).order_by(Image.page)

    # Get list of tags for this title
    tags = Tag.select(Tag,TagRelation,Volume).join(TagRelation).join(Volume).where(Volume.id == title_id).order_by(Tag.name)
    
    # pass list of thumbnails to template
    return render_template("title.html",title=volume.title,id=str(title_id),thumbs=thumbs, tags=tags)

# Render individual page image

@app.route('/page/<int:title_id>/<int:page_num>')
def page(title_id, page_num):

    # DB query to get archive file corresponding to title ID
    # and member file corresponding to page number

    # Get title information
    try:
        volume = Volume.get(Volume.id == title_id)
    except Volume.DoesNotExist:
        abort(404)

    # Get page information
    try:
        page = Image.select().join(Volume).where((Volume.id == title_id) & (Image.page == page_num)).get()
    except Image.DoesNotExist:
        abort(404)

    if volume.filetype == 'zip':

        # TODO: Error check on archive open
        z = zipfile.ZipFile(INPUT_PATH+volume.filename)
        
        # Get page binary data
        # TODO: Error checking
        foo = z.read(page.filename)
        
        z.close()
  
    # Return extracted image to browser
        return send_file(BytesIO(foo), mimetype=page.mimetype)

    elif volume.filetype == 'rar':
    
        # TODO: Error check on archive open
        z = rarfile.RarFile(INPUT_PATH+volume.filename)
        
        # Get page binary data
        # TODO: Error checking
        foo = z.read(page.filename)
        
        z.close()

    # Return extracted image to browser
        return send_file(BytesIO(foo), mimetype=page.mimetype)

    # unrecognised archive type
    else:
        abort(500)

# Test image display auto-size (responsive)
@app.route('/auto/<int:title_id>/<int:page_num>')
def autotest(title_id, page_num):

    # Pass image details to HTML/CSS page which should responsively autoscale
    # prep for implementation of image slider for page view

    return render_template("autotest.html", title_id=title_id, page_num=page_num)


# Test Unslider display
@app.route('/slide/<int:title_id>')
def slide(title_id):

    # Get title information
    try:
        volume = Volume.get(Volume.id == title_id)
    except Volume.DoesNotExist:
        abort(404)

    # Get list of images for this title
    pages = Image.select(Image,Volume).join(Volume).where(Volume.id == title_id).order_by(Image.page)

    # Pass volume and page details to Unslider template
    return render_template("slider.html", title_id=title_id, volume=volume, pages=pages)

# Error handling

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(errror):
    db.session.rollback()
    return render_template("500.html"), 500

