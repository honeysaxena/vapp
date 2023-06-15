from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from videoapp.config import settings

DB_PASSWORD_UPDATED = quote_plus(settings.db_password)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{DB_PASSWORD_UPDATED}@{settings.db_hostname}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



'''
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='api',
                                 user='postgres', password='Hforu2S@pa', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as err:
        print("Connecting to database failed")
        print("Error: ", err)
'''   
     

