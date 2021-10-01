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
        return render_template("error.html", response='Tag '+tag_id+' does not exist')

    # Filter Volume on given Tag ID

    t = Volume.select().join(Tag).where(Tag.id == tag_id).order_by(Volume.title)
    return render_template("tag.html", tags=tags, title=t)

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):

    """
    Edit Tag tag_id in DB
    """

    try:
        tag = Tag.get(id == tag_id)
    except Tag.DoesNotExist:
        return render_template("error.html", response='Tag '+tag_id+' does not exist')

    return render_template("tag_edit.html", tag=tag)

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):

    """
    Delete Tag tag_id from DB
    """

    # Check Tag exists

    try:
        tag = Tag.get(id == tag_id)
    except Tag.DoesNotExist:
        return render_template("error.html", response='Tag '+tag_id+' does not exist')

    # Delete Tag instance from DB

    tag.delete_instance()

    return render_template("tag_deleted.html", tag_id=tag_id)

@app.route('/filter/<filter_string>')
def filter_tags(filter_string):

    """
    Display list of titles filtered by tags
    filter_string is dot-separated list of tag IDs

    Check that each tag id exists
    """
    filter_list=[]
    filters=filter_string.split=(".")

    for x in filters:
        try:
            tag=Tag.get(id == x)
        except Tag.DoesNotExist:
            continue

        filter_list.append(x)

    # Filter titles on list of tag IDs

    t = Volume.select().join(Tag).where(Tag.id.in_(filter_list))
    return render_template("tags.html", tags=filter_list, title=t)

@app.route('/settings')
def settings():
    """Display application settings page"""

    return render_template("settings.html", settings=INPUT_PATH)

@app.route('/title/<int:title_id>')
def title(title_id):

    """
    Render title (grid of page thumbnails).
    """

    # Get title information
    try:
        volume = Volume.get(Volume.id == title_id)
    except Volume.DoesNotExist:
        render_template("error.html", response="Volume "+title_id+" does not exist")

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

    """
    Get archive file corresponding to title ID
    and member file corresponding to page number

    Returns extracted image to browser
    """

    # Get title information
    try:
        volume = Volume.get(Volume.id == title_id)
    except Volume.DoesNotExist:
        return render_template("error.html", response="Volume "+title_id+" does not exist")

    # Get page information
    try:
        page = Image.select().join(Volume).where((Volume.id == title_id)
                                                 & (Image.page == page_num)).get()
    except Image.DoesNotExist:
        return render_template("error.html", response="Image "+page_num+" does not exist")

    if volume.filetype == 'zip':

        # TODO: Error check on archive open
        z = zipfile.ZipFile(INPUT_PATH+volume.filename)

        # Get page binary data
        try:
            zf = z.read(page.filename)
        except zipfile.BadZipFile:
            return render_template("error.html", response="Bad archive file: "+volume.filename)

        z.close()

        # Return extracted image to browser
        return send_file(BytesIO(zf), mimetype=page.mimetype)

    elif volume.filetype == 'rar':

        # TODO: Error check on archive open
        rar = rarfile.RarFile(INPUT_PATH+volume.filename)

        # Get page binary data
        # There must be a cleaner way of fixing paths, but pathlib doesn't seem to work
        try:
            rarpath = str(page.filename).replace('\\','/')
            rardata = rar.read(rarpath)
        except rarfile.NoRarEntry:
            return render_template("error.html", response="No such file: "+rarpath+" in "+volume.filename)

        rar.close()

    # Return extracted image to browser
        return send_file(BytesIO(rardata), mimetype=page.mimetype)

    # unrecognised archive type
    else:
        return render_template("error.html", response="Unrecognised archive type: "+volume.filename)

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

# Test Tiny Slider display
@app.route('/tinyslide/<int:title_id>')
def tinyslide(title_id):
    """Test template for Unslider display, displays Title title_id"""

    # Get title information
    try:
        volume = Volume.get(Volume.id == title_id)
    except Volume.DoesNotExist:
        abort(404)

    # Get list of images for this title
    pages = Image.select(Image, Volume).join(Volume).where(
        Volume.id == title_id).order_by(Image.page)

    # Pass volume and page details to Tiny Slider template
    return render_template("tinyslider.html", title_id=title_id, volume=volume, pages=pages)

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
