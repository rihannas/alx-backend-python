#!/usr/bin/env python3
'''create a decorator that logs database queries executed by any function'''

import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    def wrapper(*args, **kwargs):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = kwargs.get('query') or (args[0] if args else None)
        print(f"[{now}] Executing SQL query: {query}")
        
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
