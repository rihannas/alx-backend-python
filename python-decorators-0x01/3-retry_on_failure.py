#!/usr/bin/env python3
"""Objective: create a decorator that retries database operations if they fail due to transient errors"""
import time
import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try: 
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn):
            attempt = 0
            while attempt < retries:
                try:
                    return func(conn)
                except Exception as e:
                    attempt+=1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("Max retries reached. Operation failed.")
                        raise
        return wrapper
    return decorator



# This is a nested decorator
@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)



"""Notes"""
'''
@retry_on_failure(retries=3, delay=1) is a decorator with parameters.
To make this possible, the outer function (retry_on_failure)
receives the parameters (retries, delay), and then returns the actual decorator (decorator(func)),
which wraps your target function.

Layer-by-layer:
retry_on_failure(...) → returns a decorator
decorator(func) → returns the wrapper
wrapper(*args, **kwargs) → calls your function, with retry logic

It’s a pattern called a parameterized decorator.
'''