from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_HOST, DB_USER, DB_PASS, DB_NAME

meta = MetaData()
engine = create_engine(f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}", encoding="utf-8", echo=True)

Session = sessionmaker(bind=engine)
session = Session()
users = Table('users', meta,
              Column('id', Integer, primary_key=True),
              Column('telegramId', Integer, nullable=False, unique=True),
              Column('username', String(34), nullable=True),
              Column('firstName', String(64), nullable=True),
              Column('lastName', String(64), nullable=True),
              Column('status', Boolean)
              )

directions = Table('directions', meta,
                   Column('id', Integer, primary_key=True),
                   Column('direction', String(20), unique=True),
                   Column('count', Integer),
                   )
Base = meta
