import sqlite3

conn=sqlite3.connect('database.db')
cursor = conn.cursor()

   
   
# Execute SQL statements to create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        timing TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cargo (
        id INTEGER PRIMARY KEY,
        weight REAL NOT NULL,
        source TEXT NOT NULL,
        destination TEXT NOT NULL
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()