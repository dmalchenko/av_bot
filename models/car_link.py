# coding=utf-8

import time
from sqlalchemy import Column, String, Integer
from models.base import Base


class CarLink(Base):
    __tablename__ = 'car_link'

    id = Column(Integer, primary_key=True)
    link = Column(String)
    av_id = Column(Integer)
    price_usd = Column(Integer)
    price_byn = Column(Integer)
    created_at = Column(Integer)
    updated_at = Column(Integer)

    def __init__(self, link, av_id, price_usd, price_byn):
        self.link = link
        self.av_id = av_id
        self.price_usd = price_usd
        self.price_byn = price_byn
        self.created_at = int(time.time())
        self.updated_at = int(time.time())
