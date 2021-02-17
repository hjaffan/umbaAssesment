


import requests
import os
from flask import Flask, current_app

app = Flask(__name__, instance_relative_config=True, template_folder='templates')

if os.getenv('DATABASE_TYPE') == "postgres":
    import psycopg2 as db
    from psycopg2 import DataError as dberror
    from urllib.parse import urlparse
    postgres_enabled = True
else:
    from sqlite3 import Error as dberror
    import sqlite3 as db
    postgres_enabled = False


db_name = os.path.join(app.instance_path, 'test.db')
github_auth_token = os.getenv('GITHUB_AUTH_TOKEN')
number_of_users = os.getenv('NUMBER_OF_USERS', 150)


def _conn_init():
    if postgres_enabled:
        database_url = os.getenv('DATABASE_URL')
        result = urlparse(database_url)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port
        connection = db.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
        return connection
    else:
        return db.connect(db_name)


def main(auth_token, number_of_users):
    user_params = int(number_of_users)
    loop_number = int(user_params / 100)
    since_number = ''
    if user_params > 100:
        for count in range(loop_number):
            r = call_and_persist_return(auth_token, "per_page=100", since_number)
            try:
                since_number = 'since={}'.format(r[99]['id'])
            except IndexError as e:
                since_number = ''
        per_page = "per_page={}".format((user_params - (loop_number * 100)))
        call_and_persist_return(auth_token, per_page, since_number)
    else:
        per_page = "per_page={}".format(user_params)
        call_and_persist_return(auth_token, per_page)


def call_and_persist_return(auth_token, per_page_param, since_number_param=''):
    url = 'https://api.github.com/users'
    headers = {'Authorization': 'token %s' % auth_token}
    queries = "{}&{}".format(per_page_param, since_number_param)
    complete_url = "{}?{}".format(url, queries)
    r = requests.get(complete_url, headers=headers)
    persist_users(r.json())
    return r.json()


def persist_users(users):
    db_setup()
    conn = _conn_init()
    cursor = conn.cursor()
    try:

        for user in users:

            if postgres_enabled:
                sql = '''INSERT INTO GITHUB_USERS(USERNAME, ID, IMAGE_URL, TYPE, PROFILE_URL) 
                VALUES(%s,%s,%s,%s,%s)
                '''
            else:
                sql = '''INSERT INTO GITHUB_USERS(USERNAME, ID, IMAGE_URL, TYPE, PROFILE_URL) 
                VALUES(?,?,?,?,?)
                '''
            cursor.execute(sql, (user['login'], int(user['id']), user['avatar_url'], user['type'], user['html_url']))
            conn.commit()
    except db.IntegrityError:
        conn.rollback()
        if postgres_enabled:
            sql_update = '''UPDATE GITHUB_USERS
            SET USERNAME = %s,
                ID = %s,
                IMAGE_URL = %s,
                TYPE = %s,
                PROFILE_URL = %s
            WHERE
                ID = %s
            '''
        else:
            sql_update = '''UPDATE GITHUB_USERS
            SET USERNAME = ?,
                ID = ?,
                IMAGE_URL = ?,
                TYPE = ?,
                PROFILE_URL = ?
            WHERE
                ID = ?
            '''
        cursor.execute(sql_update,
                       (user['login'], int(user['id']), user['avatar_url'], user['type'], user['html_url'], int(user['id'])))
        conn.commit()
    finally:
        conn.close()


def db_setup():
    conn = _conn_init()
    cursor = conn.cursor()
    try:

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
        conn.commit()
    finally:
        cursor.close()


def _create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = _conn_init()
        return conn
    except dberror as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    _create_connection()
    main(github_auth_token, number_of_users)
