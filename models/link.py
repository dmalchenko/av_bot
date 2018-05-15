# coding=utf-8

from sqlalchemy import Column, String, Integer, SmallInteger
from models.base import Base


class Link(Base):
    __tablename__ = 'link'

    id = Column(Integer, primary_key=True)
    link = Column(String)
    status = Column(SmallInteger)

    def __init__(self, link):
        self.link = link
        self.status = 10
