# -*- coding: utf-8 -*-

import requests
import telebot
import config
import time
from bs4 import BeautifulSoup
from models.db import filter_new_cars, save_cars, get_active_links


def get_data(parse_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/66.0.3359.139 Safari/537.36',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://cars.av.by/audi/a6-c4?sort=date&order=desc',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'ga=GA1.2.931458772.1525532604; _ym_uid=1525532604500478246; '
                  '__gfp_64b=6w62gMGAG9uhDzUs7VQXhqWaiTIczSs5mKtjBRcOekf.a7; _ga=GA1.3.931458772.1525532604; '
                  '_gid=GA1.2.1564219294.1525719036; PHPSESSID=ff018aoibudm1g76b8p0s17947; '
                  '_gid=GA1.3.1564219294.1525719036; adbm_depth=4; '
                  'pa=1525719040849.8070.33124171385283185cars.av.by0.7367759598447212+4',

    }
    r = requests.get(parse_url, headers=headers)
    return r.text


def get_cars(html_for_parse):
    soup = BeautifulSoup(html_for_parse, 'html.parser')
    cars = []
    for car_div in soup.find_all('div', 'listing-item'):
        image = car_div.find('img').get('src')
        link = car_div.find('a').get('href')
        id = link.split('/')[-1]
        price_byn = car_div \
            .find('div', {'class': 'listing-item-price'}) \
            .find('strong') \
            .getText() \
            .replace(" ", "") \
            .replace("Ñ\x80.", "")
        if price_byn == '':
            price_byn = 0
        price_byn = str(int(price_byn))

        price_usd = car_div.find('div', {'class': 'listing-item-price'}).find('small').getText().replace(" ", "")
        if price_usd == '':
            price_usd = 0
        price_usd = str(int(price_usd))
        cars.append({'av_id': int(id), 'link': link, 'price_usd': price_usd, 'price_byn': price_byn, 'image': image})
    return cars


def filter_cars(cars):
    ids = []
    for car in cars:
        ids.append(car['av_id'])

    new_ids = filter_new_cars(ids)

    result = []
    for car in cars:
        if car['av_id'] in new_ids:
            result.append(car)

    return result


def send_message(cars):
    bot = telebot.TeleBot(config.token)
    for car in cars:
        bot.send_message(config.chat_id, car['price_usd'] + '$ ' + car['link'])


if __name__ == '__main__':
    print('Start parser')
    start_time = time.time()

    urls = get_active_links()
    for url in urls:
        html = get_data(url.link)
        cars = get_cars(html)
        cars = filter_cars(cars)
        save_cars(cars)
        send_message(cars)
        print(cars)

    run_time = time.time() - start_time
    print('Stop parser')
    print('Total time: ', round(run_time, 3), 'sec')
