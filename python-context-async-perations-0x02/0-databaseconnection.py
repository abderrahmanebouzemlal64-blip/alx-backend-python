import sqlite3

class DatabaseConnection:
    def __init__(self, db):
        self.db = db
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT * FROM users;')
        return self.cursor.fetchall()
    

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

with DatabaseConnection('users.db') as res:
    print(res)
