import hashlib
import psycopg


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class DictPasswordStorage:
    def __init__(self):
        self.users = {}

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
    def __init__(self, dbname, db_user, db_password):
        self.connection = psycopg.connect(
            dbname=dbname,
            user=db_user,
            password=db_password,
            host="127.0.0.1",
            autocommit=True
        )
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("CREATE DATABASE cat_clinic;", prepare=True)
        except psycopg.errors.DuplicateDatabase:
            pass
        try:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id serial,
            username varchar(50) not null PRIMARY KEY,
            password varchar(256) not null);""", prepare=True)
        except:
            print("sad")


    def add(self, username, password):
        #check if the user exists, return false if it does
        username_check = ("SELECT 1 FROM users"
                          + " WHERE username = '"
                          + username + "';")
        result = self.cursor.execute(username_check, prepare=True).fetchone()
        if result:
            return False
        add_sql = ("INSERT INTO users VALUES("
                    +"DEFAULT, '"
                    + username + "', '"
                    + str(hash_password(password)) + "');")
        self.cursor.execute(add_sql, prepare=True)
        result1 = self.cursor.execute("SELECT * FROM users;", prepare=True).fetchall()
        print(result1)

    def change_password(self, username, password):
        self.cursor.execute("SELECT password FROM users" +
                     " WHERE '" +
                     username + "'= username;", prepare=True)
        pwd_in_db = self.cursor.fetchall()
        if pwd_in_db == password:
            new_password = input("enter new password: ")
            update_sql = ("UPDATE TABLE users" +
                        " SET password = '" + str(hash_password(new_password)) +
                        "' WHERE username = '" + username + "';")
            self.cursor.execute(update_sql, prepare=True)

    def check(self, username, password):
        username_check = ("SELECT 1 FROM users"
                          + " WHERE username = '"
                          + username + "';")
        result = self.cursor.execute(username_check, prepare=True).fetchone()

        # if user not in database -> false
        if result is None:

            return False

        check_pwd = ("SELECT password FROM users" +
                     " WHERE username = '" + username + "';")

        fetched_pwd = self.cursor.execute(check_pwd, prepare=True).fetchone()
        print(str(fetched_pwd)[2:-3])
        print(str(hash_password(password)))

        if str(fetched_pwd)[2:-3] == hash_password(password):
            print(1)
            return True

if __name__ == '__main__':
    db = PasswordDB("cat_clinic", "postgres", "")
