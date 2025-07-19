#!/usr/bin/env python3

'''create a class based context manager to handle opening and closing database connections automatically'''

import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

with DatabaseConnection('user.db') as db:
    db.execute('''SELECT * FROM users''')