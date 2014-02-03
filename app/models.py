#!/usr/bin/env python

from config import *
from peewee import *
import datetime

# define database
db = SqliteDatabase(DB_FILE)

# create base model class that application models will extend

class BaseModel(Model):
    class Meta:
        database = db

class Volume(BaseModel):
    title = CharField()
    md5 = CharField()
    type = CharField()
    num = IntegerField()
    added = DateTimeField(default=datetime.datetime.now)
    viewed = DateTimeField(default=datetime.datetime.now)
    comments = TextField()

class Tag(BaseModel):
    name = CharField()
    descr = CharField()

class TagRelation(BaseModel):
    relVolume = ForeignKeyField(Volume)
    relTag = ForeignKeyField(Tag)

class Image(BaseModel):
    volume = ForeignKeyField(Volume, related_name='images')
    page = IntegerField()
    path = CharField()
    thumb = CharField(max_length=512)
