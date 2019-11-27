from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgres://postgres:123@localhost:5432/", echo=True)

Base = declarative_base()
Session = sessionmaker(Base)
session = Session()

class User(Base):
    __tablename__ = 'users'
    email = Column(String, primary_key=True)
    password = Column(String)
    name = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)