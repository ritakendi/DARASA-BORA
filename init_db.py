import sqlite3
connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

# cur = connection.cursor()

# cur.execute("INSERT INTO posts (username, password) VALUES (?, ?)",
#             ('first post', 'content for the first post')
#             )
# cur.execute('INSERT INTO posts (username, password) VALUES(?,?)',
#             ('second post', 'content for the second post')
#             )

# connection.commit()
connection.close()
