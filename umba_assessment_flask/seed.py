import sqlite3
from sqlite3 import Error
import requests
import os
from flask import Flask

class Seed:

    def __init__(self, db_name):
        self.db_name = db_name

    def _conn_init(self):
        return sqlite3.connect(self.db_name)

    def main(self, auth_token, number_of_users):
        user_params = int(number_of_users)
        loop_number = int(user_params / 100)
        since_number = ''
        if user_params > 100:
            for count in range(loop_number):
                r = self.call_and_persist_return(auth_token, "per_page=100", since_number)
                try:
                    since_number = 'since={}'.format(r[99]['id'])
                except IndexError as e:
                    since_number = ''
            per_page = "per_page={}".format((user_params - (loop_number * 100)))
            self.call_and_persist_return(auth_token, per_page, since_number)
        else:
            per_page = "per_page={}".format(user_params)
            self.call_and_persist_return(auth_token, per_page)

    def call_and_persist_return(self, auth_token, per_page_param, since_number_param=''):
        url = 'https://api.github.com/users'
        headers = {'Authorization': 'token %s' % auth_token}
        queries = "{}&{}".format(per_page_param, since_number_param)
        complete_url = "{}?{}".format(url, queries)
        r = requests.get(complete_url, headers=headers)
        self.persist_users(r.json())
        return r.json()

    def persist_users(self, users):
        self.db_setup()
        conn = self._conn_init()
        try:
            conn = self._conn_init()
            cursor = conn.cursor()
            for user in users:
                sql = '''INSERT INTO GITHUB_USERS(USERNAME, ID, IMAGE_URL, TYPE, PROFILE_URL) 
                VALUES(?,?,?,?,?)
                '''
                cursor.execute(sql,
                               (user['login'], int(user['id']), user['avatar_url'], user['type'], user['html_url']))
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
            cursor.execute(sql_update,
                           (user['login'], int(user['id']), user['avatar_url'], user['type'], user['html_url']))
            conn.commit()
        finally:
            conn.close()

    def db_setup(self):
        conn = self._conn_init()
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
        finally:
            cursor.close()

    def _create_connection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = self._conn_init()
            return conn
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()


if __name__ == '__main__':
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    db_name = os.path.join(app.instance_path, os.getenv('DB_NAME', '../instance/test.db'))
    github_auth_token = os.getenv('GITHUB_AUTH_TOKEN')
    number_of_users = os.getenv('NUMBER_OF_USERS', 150)
    sd = Seed(db_name=db_name)
    sd.main(github_auth_token, number_of_users)