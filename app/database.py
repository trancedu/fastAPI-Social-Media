from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}\
        /{settings.database_name}"
print(SQLALCHEMY_DATABASE_URL)
# create an engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# base class
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# import time 
# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", 
#                                 database="fastapi", 
#                                 user="postgres", 
#                                 password="password",
#                                 cursor_factory=RealDictCursor)    
#         cursor = conn.cursor()
#         print("Database connected successfully")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("error: ", error)
#         time.sleep(2)