# -*- coding: utf-8 -*-

import config
import telebot
import requests
from bs4 import BeautifulSoup


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


def get_last_link():
    file = open('last.txt', 'r')
    result = file.read()
    file.close()
    return result


def set_last_link(value):
    file = open('last.txt', 'w')
    file.write(value)
    file.close()


def send_bot_message(link):
    bot = telebot.TeleBot(config.token)
    bot.send_message(307796085, link)


def get_cars(html_for_parse):
    soup = BeautifulSoup(html_for_parse, 'html.parser')
    last_link = get_last_link()
    for car_div in soup.find_all('div', 'listing-item'):
        link = car_div.find('a').get('href')
        if last_link == link:
            break
        else:
            send_bot_message(link)
            set_last_link(link)
            break


if __name__ == '__main__':
    url = 'https://cars.av.by/search?brand_id%5B0%5D=6&model_id%5B0%5D=15&year_from=&year_to=&currency=USD&price_from' \
            '=&price_to=&body_id=&engine_type=2&engine_volume_min=&engine_volume_max=&driving_id=&mileage_min' \
            '=&mileage_max=&region_id=&interior_material=&interior_color=&exchange=&search_time='

    html = get_data(url)
    get_cars(html)
