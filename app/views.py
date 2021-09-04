"""
Yomiko Comics Reader
(c) 2016-2020 Kyubi Systems: www.kyubi.co.uk
"""

import zipfile
from io import BytesIO

import rarfile
from flask import Flask, abort, render_template, send_file

from app.config import INPUT_PATH
from app.models import Volume, Tag, TagRelation, Image


app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

# List of titles

@app.route('/view/list')
def title_list():

    vols = Volume.select().order_by(Volume.title)

    return render_template("list.html", vols=vols)


@app.route('/view/thumbs')
def thumb_list():

    vols = Volume.select().order_by(Volume.title)

    return render_template("thumbs.html", vols=vols)

# ---- Tag operations -----

@app.route('/tags')
def all_tags():

    """
    Show all tags
    """

    tags = Tag.select().order_by(Tag.name)

    return render_template("tags.html", tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):

    """
    Show titles associated with given tag tag_id
    """

    try:
        tags = Tag.select().where(Tag.id == tag_id).order_by(Tag.name)
    except Tag.DoesNotExist:
        abort(404)

    return render_template("tags.html", tags=tags)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):

    """
    Edit Tag tag_id in DB
    """

    try:
        tag = Tag.get(id == tag_id)
    except Tag.DoesNotExist:
        abort(404)

    return render_template("tags.html", tags=tag)

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):

    """
    Delete Tag tag_id from DB
    """

    try:
        tag = Tag.get(id == tag_id)
    except Tag.DoesNotExist:
        abort(404)

    return render_template("tags.html", tags=tag)

@app.route('/filter/<filter_string>')
def filter_tags(filter_string):

    """
    Display list of titles filtered by tags
    filter_string is dot-separated list of tag IDs
    """

    # TODO: Check how to do filter search on titles

    return render_template("tags.html")

@app.route('/settings')
def settings():
    """Display application settings page"""

    return render_template("settings.html")

@app.route('/title/<int:title_id>')
def title(title_id):

    """
    Render title (grid of thumbnails).
    TODO: Image 0 as blurred CSS background?
    """

    # Get title information
    try:
        volume = Volume.get(Volume.id == title_id)
    except Volume.DoesNotExist:
        abort(404)

    # Get list of images for this title
    thumbs = Image.select(Image, Volume).join(Volume).where(Volume.id == title_id).order_by(Image.page)

    # Get list of tags for this title
    tags = Tag.select(Tag, TagRelation, Volume).join(TagRelation).join(Volume).where(Volume.id == title_id).order_by(Tag.name)

    # pass list of thumbnails to template
    return render_template("title.html", title=volume.title,
                           id=str(title_id), thumbs=thumbs, tags=tags)

# Render individual page image

@app.route('/page/<int:title_id>/<int:page_num>')
def page_image(title_id, page_num):

    """Get archive file corresponding to title ID
    and member file corresponding to page number

    Returns extracted image to browser"""

    # Get title information
    try:
        volume = Volume.get(Volume.id == title_id)
    except Volume.DoesNotExist:
        abort(404)

    # Get page information
    try:
        page = Image.select().join(Volume).where((Volume.id == title_id)
                                                 & (Image.page == page_num)).get()
    except Image.DoesNotExist:
        abort(404)

    if volume.filetype == 'zip':

        # TODO: Error check on archive open
        z = zipfile.ZipFile(INPUT_PATH+volume.filename)

        # Get page binary data
        # TODO: Error checking
        zf = z.read(page.filename)

        z.close()

        # Return extracted image to browser
        return send_file(BytesIO(zf), mimetype=page.mimetype)

    elif volume.filetype == 'rar':

        # TODO: Error check on archive open
        rar = rarfile.RarFile(INPUT_PATH+volume.filename)

        # Get page binary data
        # TODO: Error checking
        rardata = rar.read(page.filename)

        rar.close()

    # Return extracted image to browser
        return send_file(BytesIO(rardata), mimetype=page.mimetype)

    # unrecognised archive type
    else:
        abort(500)

# Test image display auto-size (responsive)
@app.route('/auto/<int:title_id>/<int:page_num>')
def autotest(title_id, page_num):
    """Test template for responsive autoscaling, displays Title title_id, page page_num

    Pass image details to HTML/CSS page which should responsively autoscale
    prep for implementation of image slider for page view"""

    return render_template("autotest.html", title_id=title_id, page_num=page_num)


# Test Unslider display
@app.route('/slide/<int:title_id>')
def slide(title_id):
    """Test template for Unslider display, displays Title title_id"""

    # Get title information
    try:
        volume = Volume.get(Volume.id == title_id)
    except Volume.DoesNotExist:
        abort(404)

    # Get list of images for this title
    pages = Image.select(Image, Volume).join(Volume).where(
        Volume.id == title_id).order_by(Image.page)

    # Pass volume and page details to Unslider template
    return render_template("slider.html", title_id=title_id, volume=volume, pages=pages)

# Error handling

@app.errorhandler(404)
def page_not_found(error):
    """Error handler for 404 Page not Found"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    """Error handler for 500 Internal Error"""
    #db.session.rollback()
    return render_template("500.html"), 500
