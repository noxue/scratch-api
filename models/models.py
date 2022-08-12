
from sqlalchemy import Column, String, create_engine, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine("sqlite:///test.db")

Session = sessionmaker()
Session.configure(bind=engine)


session = Session()

Base = declarative_base(engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(50))
    create_time = Column(DateTime, default=datetime.now)


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(50))
    data = Column(Text(255))
    create_time = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))


tables = [User.__table__, Project.__table__]


# Base.metadata.drop_all(tables=tables)
# Base.metadata.create_all(tables=tables)
