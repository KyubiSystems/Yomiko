#!/usr/bin/env python
"""
Yomiko Comics Reader
(c) 2014 Kyubi Systems: www.kyubi.co.uk
"""
from models import *


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
