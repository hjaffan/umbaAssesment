import sqlite3

from flask import current_app, g
from umba_assessment_flask import seed


def init_db(github_auth, database="../instance/test.db", number_of_users=150):
    initial_db = seed.Seed(database)
    initial_db.main(github_auth, number_of_users)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def get_all_profiles(offset=0, per_page=25):
    db = get_db()
    cursor = db.cursor()
    users = cursor.execute('SELECT USERNAME, IMAGE_URL, TYPE, PROFILE_URL FROM GITHUB_USERS').fetchall()

    return len(users), users[offset: offset + per_page]


def get_single_user(username):
    db = get_db()
    cursor = db.cursor()
    found_users = cursor.execute(
        'SELECT USERNAME, IMAGE_URL, TYPE, PROFILE_URL FROM GITHUB_USERS WHERE USERNAME LIKE \'%{}%\''.format(
            username)).fetchall()

    return found_users
