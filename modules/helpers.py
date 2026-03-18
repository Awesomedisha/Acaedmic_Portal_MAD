import sqlite3
import os
from flask import g

def get_db_path():
    # Vercel filesystem is read-only. We must use /tmp for SQLite.
    if os.environ.get('VERCEL'):
        tmp_path = '/tmp/portal.db'
        # Lazy initialize if on Vercel and file doesn't exist
        if not os.path.exists(tmp_path):
            from database.init_db import init_database
            init_database()
        return tmp_path
    
    return os.path.join(os.path.dirname(__file__), '..', 'database', 'portal.db')

def get_db():
    if 'db' not in g:
        db_path = get_db_path()
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
