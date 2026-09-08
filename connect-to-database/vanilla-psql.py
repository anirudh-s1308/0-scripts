import psycopg2

# establish connection using postgres credentials

conn = psycopg2.connect(
    host="localhost",
    database="my_database",
    user="postgres",
    password="my_password",
    port="5432"
)

try:
    # create a connection to the database
    with conn.connect() as cursor:

        # execute sql
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO users (name) VALUES ('Alice')")

        # commit if writing to db
        cursor.commit()

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print(users)


finally:
    # manullay close connection as psycopg2 acts differently for with statement
    conn.close()
    