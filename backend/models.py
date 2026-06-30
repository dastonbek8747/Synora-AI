import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from db_conn import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    session_id = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


class Images(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    session = Column(String, ForeignKey('users.session_id'))
    image_path = Column(String, nullable=False, index=True)
    image_name = Column(String, nullable=False, index=True)
    create_date = Column(Date, default=datetime.datetime.now)


class Videos(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.session_id'))
    video_path = Column(String, nullable=False, index=True)
    video_name = Column(String, nullable=False, index=True)
    create_date = Column(Date, default=datetime.datetime.now)


class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.session_id'))
    file_path = Column(String, nullable=False, index=True)
    file_name = Column(String, nullable=False, index=True)
    create_date = Column(Date, default=datetime.datetime.now)
