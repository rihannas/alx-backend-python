#!/usr/bin/env python3
'''Objective: create a decorator that caches the results of a database queries inorder to avoid redundant calls'''


import sqlite3 
import functools
import time as t

query_cache = {}
cache_time = 600

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try: 
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        now = t.time()
        query = kwargs.get('query') or (args[0] if args else None)

        if query in query_cache.keys(): 
            result, time = query_cache[query]
            if now - time < cache_time:
                print('Returning Query Results From Cache...')
                return query_cache[query]
            else:
                print("Cache expired, re-reun query")
        
        results = func(conn, *args, **kwargs)
        print(f"Executing SQL query: {query}...saving results")
        query_cache[query] = (results, now)
        print(f"Cache: {query_cache}")
        return func(conn, *args, **kwargs)
    return wrapper



@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

print('------')

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")


