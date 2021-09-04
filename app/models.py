#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2016-2020 Kyubi Systems: www.kyubi.co.uk
"""
from datetime import datetime
from peewee import Model, SqliteDatabase, CharField, IntegerField, TextField, DateTimeField,\
     BooleanField, ForeignKeyField, DoesNotExist
from app.config import DB_FILE

# define database
db = SqliteDatabase(DB_FILE)

# create base model class that application models will extend


class BaseModel(Model):
    class Meta:
        database = db


# Volume class associated with ZIP or RAR file
class Volume(BaseModel):
    title = CharField()
    filename = CharField(unique=True)
    md5 = CharField()
    filetype = CharField()
    num = IntegerField()
    comments = TextField()
    read_at = DateTimeField(null=True)
    is_favourite = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(null=True)
    deleted_at = DateTimeField(null=True)

    class Meta:
        order_by = ('title',)

    def __unicode__(self):
        return self.title + ' ' + self.filename

    def __str__(self):
        return self.title + ' ' + self.filename

    @property
    def is_read(self):
        """ Is this volume read? """
        return self.read_at is not None

# Tag class
class Tag(BaseModel):
    name = CharField(unique=True)
    descr = CharField()

    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(null=True)
    deleted_at = DateTimeField(null=True)

    class Meta:
        order_by = ('name',)

    def __unicode__(self):
        return self.name + ' ' + self.descr

    def __str__(self):
        return self.name + ' ' + self.descr


# TagRelation for many-to-many mapping between Tag and Volume
class TagRelation(BaseModel):
    relVolume = ForeignKeyField(Volume)
    relTag = ForeignKeyField(Tag)


# Image class for individual member image
class Image(BaseModel):
    volume = ForeignKeyField(Volume, on_delete='cascade', related_name='images')
    page = IntegerField()
    filename = CharField()
    mimetype = CharField()
    thumb_ok = BooleanField(default=False)  # Set True if thumbnail successfully generated

    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(null=True)
    deleted_at = DateTimeField(null=True)

    class Meta:
        order_by = ('page',)

    def __unicode__(self):
        return self.filename + ' ' + self.page

    def __str__(self):
        return self.filename + ' ' + self.page
