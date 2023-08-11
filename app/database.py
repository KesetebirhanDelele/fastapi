# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor 
# import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Specify where postgres database is located
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>' 

# Enginge is responsible for sqlalchemy to establish connection to database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session required to connect to a database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All database models will use this base class
Base = declarative_base()

# Dependency
""" The session object is kind of what's responsible for talking with the databases and so we've created this
function where we actually get a connection to our database or get a session to our database and so every
time we get a request we're going to get a session we're going be able to send sql statements to it and
then after that request is done we'll close it out and so it's as much more efficient doing
it like this by having one little function and we can just keep calling this function every time we get a
request to any of our api endpoints
"""
# Session object responsible to communicate with database.
def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()


# while True: # This code allows for repeated attempt to connect if not connected and breaks if connected remain connected.
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Target123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Connection Successful')
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print('Error: ', error)
#         time.sleep(2)   # If a connection fails, take a 2 second break before trying to re-reconnect
