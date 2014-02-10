#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""
from models import *


# Create SQLite3 tables
def create_db():

    # Define database
    db = SqliteDatabase(DB_FILE)

    # Connect to database
    db.connect()

    # Create tables
    Volume.create_table()
    Tag.create_table()
    Image.create_table()
    TagRelation.create_table()


# Empty SQLite3 tables
def truncate_db():

    # Define database
    db = SqliteDatabase(DB_FILE)

    # Connect to database
    db.connect()

    delete_query = Image.delete().where(True)
    delete_query.execute()

    delete_query = TagRelation.delete().where(True)
    delete_query.execute()

    delete_query = Tag.delete().where(True)
    delete_query.execute()

    delete_query = Volume.delete().where(True)
    delete_query.execute()

