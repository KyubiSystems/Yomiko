from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/list'):
def plist():
    return render_template("list.html")

@app.route('/tags'):
def tags():
    return render_template("tags.html")

@app.route('/settings'):
def settings():
    return render_template("settings.html")

@app.route('/title'):
def title():
    return render_template("title.html")

@app.route('/page'):
def page():
    return render_template("page.html")
