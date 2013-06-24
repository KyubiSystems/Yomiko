import sqlite3
from flask import g

DATABASE = './db/database.db' # Should set this in config

# Database initialisation
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

# Database close
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Declare row_factory
# Where is this supposed to go?
db.row_factory - sqlite3.Row

# General DB query function
def query_db(query, args=(), one=False):
    cur = get_db().execute(query,args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
