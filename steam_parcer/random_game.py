import requests
from bs4 import BeautifulSoup
import json
from content_randomgame import content_type
from random import randint, randrange


def find_max_starter(content, max_starter=0):
    page_link_json = content_type[content].replace('+', f'{max_starter}')
    url = f'{page_link_json}'
    request = requests.get(url)
    data_page = request.content

    while json.loads(data_page):
        if json.loads(data_page)['results_html'] == '':
            return max_starter
        else:
            max_starter += 15
            return find_max_starter(content, max_starter)


def load_data(start, content):
    page_link_json = content_type[content].replace('+', f'{start}')
    url = f'{page_link_json}'
    request = requests.get(url)
    data = request.content

    if json.loads(data)['results_html'] != '':
        html_page = json.loads(data)
        soup = BeautifulSoup(html_page['results_html'], 'lxml')

        rand_game = randint(0, len(soup.find_all(class_='tab_item_name')))

        game_name = soup.find_all(class_='tab_item_name')[rand_game].text
        game_tags = soup.find_all(class_='tab_item_top_tags')[rand_game].text
        game_link = soup.find_all(class_='tab_item')[rand_game].get('href')
        game_img_link = soup.find_all('img')[rand_game].get('src')

        game_info_dict = dict(Название=f'{game_name}', Тэги=f'{game_tags}',
                              Ссылка=f'{game_link}', Картинка=f'{game_img_link}')
        # print(game_info_dict)
        return game_info_dict


def get_data(content):
    if content == 'Популярные новинки':
        max_starter = 90
        max_start = find_max_starter('Популярные новинки', max_starter)
        return load_data(randrange(0, max_start-15, 15), 'Популярные новинки')
    elif content == 'Лидеры продаж':
        max_starter = 225
        max_start = find_max_starter('Лидеры продаж', max_starter)
        return load_data(randrange(0, max_start-15, 15), 'Лидеры продаж')
    elif content == 'Будущие продукты':
        max_starter = 240
        max_start = find_max_starter('Будущие продукты', max_starter)
        return load_data(randrange(0, max_start-15, 15), 'Будущие продукты')
    elif content == 'Во что играют другие':
        max_starter = 2900
        max_start = find_max_starter('Во что играют другие', max_starter)
        return load_data(randrange(0, max_start-15, 15), 'Во что играют другие')
