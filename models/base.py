# coding=utf-8

import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.db_string)
Session = sessionmaker(bind=engine)

Base = declarative_base()
