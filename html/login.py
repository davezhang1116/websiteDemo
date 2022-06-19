from dataclasses import dataclass
import sqlite3
from hashlib import sha256

@dataclass
class login:
    _username: str
    _password: str

    def __init__(self, _username, _password):
        self.username = _username
        self.password = _password

    def create(self):
        conn = sqlite3.connect('./database/login.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE {} (
        password TEXT""".format(self.username))
        conn.commit()
        hash = sha256(self.password.encode('utf-8')).hexdigest()

        conn = sqlite3.connect('./database/login.db')
        c = conn.cursor()
        c.execute("""INSERT INTO {} VALUES (?)""".format(self.username),hash)
        conn.commit()
        conn.close()

    def verify(self):
        conn = sqlite3.connect('./database/login.db')
        c = conn.cursor()
        c.execute("""SELECT password FROM {}""".format(self.username))
        rows = c.fetchall()
        encryptedPassword=rows[0][0]
        print(encryptedPassword)
        if encryptedPassword == sha256(self.password.encode('utf-8')).hexdigest() :
            return True
        else:
            return False
