#!/usr/bin/env python

from config import *
from peewee import *
from models import *

# Define database
db = SqliteDatabase(DB_FILE)

# Connect to database
db.connect()

# Create tables
Volume.create_table()
Tag.create_table()
Image.create_table()
