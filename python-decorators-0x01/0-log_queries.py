#!/usr/bin/env python3
'''create a decorator that logs database queries executed by any function'''

import sqlite3
import functools

def log_queries(func):
    def wrapper(*args, **kwargs):
        print('Query Logs:')
        print(f"{args}, {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
