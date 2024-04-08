import hashlib


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
