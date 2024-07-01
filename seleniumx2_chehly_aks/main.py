from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from collections import defaultdict
import lxml
import shutil
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
import time
import os
import json
import requests
import uuid
from datetime import datetime


path = 'html/full_source/'
filename = 'page-'
def get_count_pages(path):
    files = os.listdir(path)
    elements_count = len(files)
    return elements_count

def get_pages(page_max):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    # url = 'https://blizko.ru/predl/computer/computer/planshetnye_kompjutery/planshety3q?page=23'
    # driver.get(f"{url}")
    # source = driver.page_source
    # with open(f"html/smartfony/catalog_source/page-1", "w", encoding="utf-8") as file:
    #     file.write(source)
    # page_max = 1
    i = 0
    while i < page_max:
        i += 1
        url = f'https://quke.ru/shop/aksessuary/zaryadnye-ustrojstva?page={i}'
        driver.get(f"{url}")
        source = driver.page_source
        with open(f"html/catalog_source/page-{i}", "w", encoding="utf-8") as file:
            file.write(source)

    driver.quit()

def get_catalog_links():
    directory = 'html/catalog_source/'
    filename = 'page-'
    i = 0
    data = []
    domain = 'https://quke.ru'
    count_pages = get_count_pages(directory)

    while i < count_pages:
        i += 1
        print(i)
        with open(f'{directory}{filename}{i}', 'r', encoding='utf-8') as file:
            source = file.read()
            file.close()

        soup = BeautifulSoup(source, 'html.parser')
        links = soup.findAll('a', class_='b-card2-v2__name')
        for item in links:
            data.append(f'{domain}{item.get('href')}/specs#product-tabs')

    with open('json/catalog/catalog_links.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_item_page():
    options = webdriver.ChromeOptions()
    # options.add_argument("start-maximized")

    options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    with open('json/catalog/catalog_links.json', 'r', encoding='utf-8') as file:
        json_source = file.read()
        file.close()
    source = json.loads(json_source)
    i = 0
    start_time_all = datetime.now()
    for item in source:
        start_time_while = datetime.now()
        i += 1
        driver.get(f"{item}")
        time.sleep(10)
        source = driver.page_source
        with open(f"html/full_source/page-{i}", "w", encoding="utf-8") as file:
            file.write(source)
        time_save = datetime.now() - start_time_while
        print(f'[[*]] Страница {item} загружена и сохранена. Время обработки страницы: {time_save}')

    all_time = datetime.now() - start_time_all
    print(f"Общее время выполнения: {all_time}")


def get_contents():
    p = 0
    while p < get_count_pages(path):
        p += 1
        print(p)
        try:
            with open(f'{path}{filename}{p}', 'r', encoding='utf-8') as file:
                source = file.read()
                file.close()
        except:
            print('file not found')


        data = dict()
        list = []
        try:
            soup = BeautifulSoup(source, 'html.parser')

            dataTable = soup.find('div', class_='b-ch__body-col').findAll('div', class_='b-ch__block-items')

            test = dict()
            result = dict()
            block_items_names = soup.findAll('div', class_='b-ch__block-item-name')  # Тут наименования характеристик
            block_items_values = soup.findAll('div', class_='b-ch__block-item-value')  # Тут значения характеристик
            # title = block_items_values[5].get_text(strip=True).strip('?')
            # title = soup.find('span', class_='b-breadcrumbs__text').get_text()
            # title = soup.find('a', class_='b-breadcrumbs__link').find('span', class_='b-breadcrumbs__text').get_text()

            count = len(block_items_names)  # количество записей
            i = 0
            data = defaultdict(lambda: defaultdict(dict))
            while i < count:
                test[block_items_names[i].get_text(strip=True).strip('?')] = block_items_values[i].get_text(
                    strip=True).strip('?')
                i += 1

            # d = 0
            # while d < 10:
            #     d += 1
            #     title += str(1)
            #
            data = test

            #     print(data)
            #     print(title)

            with open(f'json/result/result-{p}.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)


        except Exception:
            print('item not found')


if __name__ == '__main__':
    get_pages(2)
    get_catalog_links()
    get_item_page()
    get_contents()




