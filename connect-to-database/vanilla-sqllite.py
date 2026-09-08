import sqlite3

# establish connection
with sqlite3.connect("my_database.db") as conn:

    # create a cursor to excecute sql queries
    cursor = conn.cursor()

    # execute sql
    # if writing then must commit 
    cursor = cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES ('Alice')")

    conn.commit()

    # if only reading no need to commit
    cursor.execute("SELECT * FROM users")
    users = cursor.getchall()
    print(users)

    # connection gets closed as with statement is used other manually close 
    # conn.close()