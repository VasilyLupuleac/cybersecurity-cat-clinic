import hashlib
import psycopg

def hash_password(password):
    return hashlib.sha256(password.encode())


class DictPasswordStorage:
    def __init__(self):
        self.users = {'admin': hash_password('admin')}
        # TODO change

    def add(self, username, password):
        if username in self.users:
            return False
        self.users[username] = hash_password(password)
        return True

    def change_password(self, username, password):
        if username not in self.users:
            return False
        self.users[username] = hash_password(password)
        return True

    def check(self, username, password):
        return (username in self.users and
                self.users[username] == hash_password(password))

class PasswordDB:
    def __init__(self):
        db_user = input("username for postgres: ")
        db_password = input("password for database: ")
        self.connection = psycopg.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host="localhost",
            autocommit=True
        )
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("CREATE DATABASE passwords;")
        except psycopg.errors.DuplicateDatabase:
            pass
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id serial,
            username varchar(50) not null PRIMARY KEY,
            password varchar(256) not null);""")

            #use indexing??

        except:
            pass

    def add(self, username, password):
        add_sql = ("INSERT INTO users VALUES("
                    +"DEFAULT, "
                    + username + ", "
                    + hash_password(password) + ");")
        self.cursor.execute(add_sql)

    def change_password(self, username, password):
        self.cursor.execute("SELECT password FROM users" +
                     "WHERE " +
                     username + "= username;")
        pwd_in_db = self.cursor.fetchall()
        if pwd_in_db == password:
            new_password = input("enter new password: ")
            update_sql = ("UPDATE TABLE users" +
                        "SET password = " + hash_password(new_password) +
                        "WHERE username = " + username + ";")
            self.cursor.execute(update_sql)

    def check(self):
        pass
        #TODO

"""
if __name__ == '__main__':
    password_db = PasswordDB()
"""