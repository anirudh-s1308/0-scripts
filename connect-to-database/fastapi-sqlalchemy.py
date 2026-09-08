from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

"""
   1. The ORM (SQLAlchemy) = The Translator
This is what actually converts your Python classes into SQL queries. When you write db.query(User).all(), the ORM looks at your Python code and generates the raw string: "SELECT * FROM users;".

2. The Engine = The Manager
The engine receives that raw SQL string from the ORM. The engine is responsible for the Connection Pool. It says, "Okay, I have a SQL query ready to go. Let me grab one of the open connections from my pool so I can send this to the database."

3. The Driver = The Delivery Person
The driver (psycopg2, sqlite3) gets handed the SQL string by the engine. The driver does not know anything about Python classes. Its only job is to take that raw SQL string, pack it up into network bytes, send it across the internet/local network to PostgreSQL, wait for the response, and hand the raw data back to the engine.

4. The Database = The Kitchen
Receives the SQL from the driver, executes it, and sends the raw data back.
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