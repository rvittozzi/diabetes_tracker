import sqlite3

# Function to create a users table in a given database connection
def create_users_table(cursor):
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT);'''
    )

# Connect to the first database (this will create the file if it does not exist)
conn1 = sqlite3.connect("users.db")
cursor1 = conn1.cursor()
# Create users table in the first database
create_users_table(cursor1)
# Commit changes and close the first connection
conn1.commit()
conn1.close()

# Connect to the second database (this will create the file if it does not exist)
conn2 = sqlite3.connect("blood_sugar_entry.db")
cursor2 = conn2.cursor()
# Create users table in the second database
create_users_table(cursor2)
# Commit changes and close the second connection
conn2.commit()
conn2.close()
