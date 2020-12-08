import psycopg2
import os


class Dbase:
    def __init__(self):
        self.connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        self.cursor = self.connection.cursor()

    def close_connection(self):
        return self.cursor.close(), self.connection.close()


    def create_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS users;')
        query = """CREATE TABLE users (
                id SERIAL PRIMARY KEY, 
                fname VARCHAR(40) NOT NULL,
                lname VARCHAR(40) NOT NULL,
                idtel INT NOT NULL,
                status INT NOT NULL);"""
        return self.cursor.execute(query)

    def add_user(self, value):
        self.cursor
        self.connection.autocommit = True
        query = "INSERT INTO users (fname, lname, idtel, status) VALUES (%s, %s, %s, %s);"
        return self.cursor.execute(query, value)

    def user_exists(self, value):
        self.cursor
        query = "select * from users where fname=%s and lname=%s and idtel=%s;"
        self.cursor.execute(query, value)
        result = self.cursor.fetchall()
        return bool(result)

    def obnovit_podpisky(self, value):
        self.connection.autocommit = True
        self.cursor
        query = "update users set status=1 where idtel=%s;"
        return self.cursor.execute(query, value)

    def otpiska(self, value):
        self.cursor
        self.connection.autocommit = True
        query = "update users set status=0 where idtel=%s;"
        return self.cursor.execute(query, value)


    def all_users(self):
        query = "select idtel from users where status=1;"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result



