# coding=utf-8

from models.base import Session
from models.link import Link
from models.car_link import CarLink

session = Session()


def get_active_links():
    links = session.query(Link) \
        .filter(Link.status == 10) \
        .all()
    return links


def filter_new_cars(ids):
    car_links = session.query(CarLink) \
        .filter(CarLink.av_id.in_(ids)) \
        .all()

    exist_ids = []
    for new_car in car_links:
        exist_ids.append(int(new_car.av_id))
    result = list(set(ids)-set(exist_ids))
    return result


def save_cars(cars):
    for car in cars:
        session.add(CarLink(car['link'], car['av_id'], car['price_usd'], car['price_byn']))
    session.commit()
    session.close()
