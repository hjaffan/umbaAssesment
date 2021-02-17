from flask import current_app, g
import os

if os.getenv('DATABASE_TYPE') == "postgres":
    import psycopg2 as db
    from urllib.parse import urlparse
    postgres_enabled = True
else:
    import sqlite3 as db
    postgres_enabled = False

def get_db():
    if 'db' not in g:
        if postgres_enabled:
            database_url = os.getenv('DATABASE_URL')
            result = urlparse(database_url)
            username = result.username
            password = result.password
            database = result.path[1:]
            hostname = result.hostname
            port = result.port
            g.db = db.connect(
                database=database,
                user=username,
                password=password,
                host=hostname,
                port=port
            )
        else:
            g.db = db.connect(
                current_app.config['DATABASE'],
                detect_types=db.PARSE_DECLTYPES
            )
            g.db.row_factory = db.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def get_all_profiles(offset=0, per_page=25):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT USERNAME, IMAGE_URL, TYPE, PROFILE_URL FROM GITHUB_USERS')
    users = cursor.fetchall()
    return len(users), users[offset: offset + per_page]


def get_single_user(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT USERNAME, IMAGE_URL, TYPE, PROFILE_URL FROM GITHUB_USERS WHERE USERNAME LIKE \'%{}%\''.format(
            username))
    found_users = cursor.fetchall()
    return found_users
