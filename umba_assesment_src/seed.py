import requests
import constants
import sqlite3
from sqlite3 import Error


def _conn_init():
    return sqlite3.connect(constants.DB_NAME)


def main(user_params=150):
    url = 'https://api.github.com/users'
    headers = {'Authorization': 'token %s' % constants.API_AUTH_TOKEN}

    pagination_count = user_params % 100
    remaining_counts = user_params % 100
    queries = 'per_page=100&since=%'
    r = requests.get(url, headers=headers)
    _persist_users(r.json())



def _persist_users(users):
    db_setup()
    try:
        conn = _conn_init()
        cursor = conn.cursor()
        for user in users:
            sql = '''INSERT INTO GITHUB_USERS(USERNAME, ID, IMAGE_URL, TYPE, PROFILE_URL) 
            VALUES(?,?,?,?,?)
            '''
            cursor.execute(sql, (user['login'], int(user['id']), user['avatar_url'], user['type'], user['html_url']))
            conn.commit()
    except sqlite3.IntegrityError:
        sql_update = '''UPDATE GITHUB_USERS
        SET USERNAME = ?,
            ID = ?,
            IMAGE_URL = ?,
            TYPE = ?,
            PROFILE_URL = ?
        WHERE
            ID = "%s"
        ''' % int(user['id'])
        cursor.execute(sql_update, (user['login'], int(user['id']), user['avatar_url'], user['type'], user['html_url']))
        conn.commit()
    finally:
        conn.close()


def db_setup():
    _create_connection()
    try:
        conn = _conn_init()
        cursor = conn.cursor()
        sql = '''CREATE TABLE IF NOT EXISTS GITHUB_USERS(
           USERNAME CHAR(50) NOT NULL,
           ID INT,
           IMAGE_URL VARCHAR(150),
           TYPE CHAR(50),
           PROFILE_URL VARCHAR(150),
           UNIQUE(ID) 
        )
        '''
        cursor.execute(sql)
    finally:
        cursor.close()


def _create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = _conn_init()
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
