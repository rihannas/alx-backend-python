#!/usr/bin/env python3

'''create a decorator that manages database transactions by automatically committing or rolling back changes'''

import sqlite3 
import functools

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # If no exception, commit changes
            return result
        except Exception as e:
            conn.rollback()  # Roll back if error
            print(f"Transaction failed: {e}")
            raise
    return wrapper


def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try: 
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')