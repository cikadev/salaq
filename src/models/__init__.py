from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgres://postgres:123@localhost:5432/bojonegoro", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()