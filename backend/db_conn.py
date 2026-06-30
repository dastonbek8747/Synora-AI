from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(url=DATABASE_URL)
Local_Sesion = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = Local_Sesion()
    try:
        yield db
    finally:
        db.close()
