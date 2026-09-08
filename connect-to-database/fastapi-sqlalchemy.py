from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

"""
    1. The Driver (The Translator)
A database driver is a low-level library that knows exactly how to communicate with a specific database server over the network.

Databases like PostgreSQL, MySQL, and Oracle all speak different "languages" (network protocols). The driver translates your Python commands into the raw bytes that a specific database understands, and translates the database's response back into Python data types.

Its job: Open a single connection, send raw SQL, and fetch results.

Examples in Python: psycopg2 (for Postgres), sqlite3 (for SQLite), mysql-connector-python (for MySQL), asyncpg (for async Postgres).

When you use it: When you are writing vanilla Python (like in the previous examples), you interact with the driver directly.

2. The Engine (The Manager)
The "engine" is a higher-level concept, most famously used by the SQLAlchemy framework. It acts as a central management system for your database connections.

The engine doesn't actually know how to talk to PostgreSQL or MySQL itself. Instead, it relies on a driver to do the actual talking. The engine's job is to make your application run efficiently at scale.

Its job:

Connection Pooling: Instead of opening and closing a new database connection for every single user request (which is very slow), the engine keeps a "pool" of open connections ready to be used.

Dialect Translation: It figures out which specific flavor of SQL to write (e.g., knowing that Postgres uses SERIAL while SQLite uses AUTOINCREMENT) before handing it to the driver.
"""


# setup sqlalchemy engine connection '

SQLALCHEMY_DATABSE_URL = "sqlite:///./my_database.db"
engine = create_engine(SQLALCHEMY_DATABSE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

Base.metadata.create_all(bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 3. Create the Database Dependency
def get_db():
    db = SessionLocal() # Open connection
    try:
        yield db        # Pass it to the route
    finally:
        db.close()      # Close connection when route finishes

# 4. Inject the database session into your route
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users