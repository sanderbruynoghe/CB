# Smappee_DatabaseQuery.py
'''Query the (default) Smappee database'''
import sqlite3

def database_query(query, database = 'Smappee_data.db'):
    '''Queries a database (string) with a given query (string) and returns tuples with output.
    The default database is the database with smappee measurements'''
    conn = sqlite3.connect(database)
    c = conn.cursor()
    return c.execute(query).fetchall()
