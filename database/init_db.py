"""
init_db.py — Run this once to set up the database and seed the default admin.
Usage: python database/init_db.py
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

def get_db_path():
    if os.environ.get('VERCEL'):
        return '/tmp/portal.db'
    return os.path.join(os.path.dirname(__file__), 'portal.db')

DB_PATH = get_db_path()
SCHEMA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'schema.sql'))


def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Load and execute schema
    with open(SCHEMA_PATH, 'r') as f:
        cursor.executescript(f.read())

    # Seed default admin user if not already present
    existing = cursor.execute(
        "SELECT id FROM users WHERE email = ?", ('admin@portal.com',)
    ).fetchone()

    if not existing:
        admin_hash = generate_password_hash('admin123')
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ('Portal Admin', 'admin@portal.com', admin_hash, 'admin')
        )
        print("✅ Default admin created: admin@portal.com / admin123")
    else:
        print("ℹ️  Admin already exists, skipping seed.")

    conn.commit()
    conn.close()
    print(f"✅ Database initialized at: {DB_PATH}")


if __name__ == '__main__':
    init_database()
