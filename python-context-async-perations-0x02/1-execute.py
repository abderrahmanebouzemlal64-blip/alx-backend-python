import sqlite3

class ExecuteQuery:
    def __init__(self, db, query, prm):
        self.db = db
        self.query = query
        self.prm = [prm]

    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.prm)
        return self.cursor.fetchall()
    

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

with ExecuteQuery('users.db', 'SELECT * FROM users WHERE age > ?', 25) as res:
    print(res)
