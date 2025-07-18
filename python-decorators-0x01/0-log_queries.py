#!/usr/bin/env python3
'''create a decorator that logs database queries executed by any function'''

def log_queries(func):
    def wrapper(*args, **kwargs):
        print('Query Logs:')
        print(f"{args}, {kwargs}")
        func(*args, **kwargs)
    return wrapper


