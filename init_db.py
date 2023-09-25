import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create table for storing user information
cursor.execute(
    '''CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT);'''
)

conn.commit()
conn.close()
