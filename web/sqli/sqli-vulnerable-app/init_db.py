import sqlite3

connection = sqlite3.connect('users.db')

with connection:
    connection.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    connection.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    connection.execute("INSERT INTO users (username, password) VALUES ('user', 'user123')")

connection.close()