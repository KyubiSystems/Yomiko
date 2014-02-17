#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""
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
    file = CharField(unique=True)
    md5 = CharField()
    type = CharField()
    num = IntegerField()
    added = DateTimeField(default=datetime.datetime.now())
    viewed = DateTimeField(default=datetime.datetime.now())
    comments = TextField()
    is_read = BooleanField(default=False)
    is_favourite = BooleanField(default=False)


class Tag(BaseModel):
    name = CharField(unique=True)
    descr = CharField()


class TagRelation(BaseModel):
    relVolume = ForeignKeyField(Volume)
    relTag = ForeignKeyField(Tag)


class Image(BaseModel):
    volume = ForeignKeyField(Volume, related_name='images')
    page = IntegerField()
    file = CharField()
    thumb_ok = BooleanField(default=False)  # Set True if thumbnail successfully generated
