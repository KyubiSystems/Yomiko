"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""

from flask import Flask, render_template

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

@app.route('/settings')
def settings():
    return render_template("settings.html")

@app.route('/title')
def title():
    return render_template("title.html")

@app.route('/page')
def page():
    return render_template("page.html")

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

