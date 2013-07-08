from flask import Flask

app = Flask(__name__)
from app import database, views

# Remove database session on shutdown

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
