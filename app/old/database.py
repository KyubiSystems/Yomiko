from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

# initialise SQLAlchemy object

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./db/database.db"
db = SQLAlchemy(app)

# begin model definition

# define Volume model class

class Volume(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256))
    md5 = db.Column(db.String(100))
    type = db.Column(db.String(10))
    num = db.Column(db.Integer)
    added = db.Column(db.DateTime)
    viewed = db.Column(db.DateTime)
    comments = db.Column(db.Text)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return '<Volume %r>' % self.title

# define Tag model class

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    descr = db.Column(db.String(256))

    def __init__(self, name, descr):
        self.name = name
        self.descr = descr

    def __repr__(self):
        return '<Tag %r>' % self.name

# define Image model class

class Image(db.Model):
    volume_id = db.Column(db.Integer, db.ForeignKey('volume.id')) # Foreign Key field
    id = db.Column(db.Integer)
    path = db.Column(db.String(512))
    thumb = db.Column(db.String(512))

    def __init__(self, path, thumb):
        self.path = path
        self.thumb = thumb

    def __repr__(self):
        return'<Image %r>' % self.id
