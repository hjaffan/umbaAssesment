import sqlite3
from sqlite3 import Error
import constants
import requests


def _conn_init():
    return sqlite3.connect(constants.DB_NAME)


def main():
    user_params = constants.NUMBER_OF_USERS
    loop_number = int(user_params / 100)
    since_number = ''
    if user_params > 100:
        for count in range(loop_number):
            r = call_and_persist_return("per_page=100", since_number)
            try:
                since_number = 'since={}'.format(r[99]['id'])
            except IndexError as e:
                since_number = ''
        per_page = "per_page={}".format((user_params - (loop_number*100)))
        call_and_persist_return(per_page, since_number)
    else:
        per_page = "per_page={}".format(user_params)
        call_and_persist_return(per_page)


def call_and_persist_return(per_page_param, since_number_param=''):
    url = 'https://api.github.com/users'
    headers = {'Authorization': 'token %s' % constants.API_AUTH_TOKEN}
    queries = "{}&{}".format(per_page_param, since_number_param)
    complete_url = "{}?{}".format(url, queries)
    r = requests.get(complete_url, headers=headers)
    persist_users(r.json())
    return r.json()


def persist_users(users):
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
        # print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
