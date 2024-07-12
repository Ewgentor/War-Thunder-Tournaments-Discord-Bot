from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup as bs
import json


def get_html(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    print("Подключаемся к сайту турниров...")
    driver.get(url=url)
    print("Собираем данные турниров...")
    button = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, 'linkLoadTournaments')))
    button.click()
    soup = bs(driver.page_source, "html.parser")
    driver.close()
    driver.quit()
    return soup


def find_type(title: str):
    if title.find("РБм") != -1 or title.find("PБм") != -1:
        return "рбм"
    elif title.find("РБ") != -1 or title.find("PБ") != -1:
        return "рб"
    elif title.find("СБ") != -1 or title.find("CБ") != -1:
        return "сб"
    else:
        return "аб"


def find_vehicle(title: str):
    if title.lower().find("авиа") != -1 or title.lower().find("jet") != -1:
        return "авиа"
    elif title.lower().find("кораб") != -1 or title.lower().find("ship") != -1:
        return "корабл"
    elif title.lower().find("танк") != -1 or title.lower().find("armor") != -1 or title.lower().find("44") != -1:
        return "наземн"
    else:
        return "смеш"


def find_players(title: str):
    if title.lower().find("1x1") != -1 or title.lower().find("1х1") != -1:
        return "1x1"
    elif title.find("2x2") != -1 or title.lower().find("2х2") != -1:
        return "2x2"
    elif title.find("3x3") != -1 or title.lower().find("3х3") != -1:
        return "3x3"
    elif title.find("4x4") != -1 or title.lower().find("4х4") != -1:
        return "4x4"
    else:
        return "5x5"


def get_tournaments(html):
    dct = {}
    for el in bs.select(html, ".row_list_tour:has(.open)"):
        a = el.select('.btn-other_bottom')[-2]["href"]
        img = el.select('.img_tournament')[0]["src"]
        title = el.select('h3')[0].text
        data = el.select('.date-tournament')[0].text
        dct[title] = {
            "date": data,
            "img_src": f"https:{img}",
            "type": find_type(title),
            "href": f"https://tss.warthunder.ru/index.php{a}",
            'veh': find_vehicle(title),
            'players': find_players(title)
        }
    print(f"Получено {len(dct)} турниров")
    return dct


def save_to_json(data: dict):
    print("Сохраняем данные в базу...")
    with open("tournaments.json", 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def read_from_json():
    with open("tournaments.json", 'r') as json_file:
        tournaments_dict = json.load(json_file)
    return tournaments_dict


def update_json():
    save_to_json(get_tournaments(get_html("https://tss.warthunder.ru/index.php?action=current_tournaments")))
    print("Готово")


if __name__ == "__main__":
    update_json()
