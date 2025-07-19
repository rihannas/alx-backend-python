#!/usr/bin/env python3

'''create a reusable context manager that takes a query as input and executes it, managing both connection and the query execution'''

import sqlite3

class ExecuteQuery:
    def __init__(self, query, db_name, params=None, ):
        self.query = query
        self.params = params
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result 

    def __exit__(self, exc_type, exc_value, traceback):
    
            self.cursor.close()
            self.conn.close()


query = "SELECT * FROM users WHERE age > ?"
params = '25'

with ExecuteQuery(query, params) as results:
    for row in results:
        print(row)
