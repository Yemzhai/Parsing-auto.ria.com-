from bs4 import BeautifulSoup
import requests
import csv
import os

# URL = 'https://auto.ria.com/newauto/marka-opel/'
HEADERS  = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36',
            'accept': '*/*'
            }
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('span', class_='mhide')
    # print(pages[-1])
    if pages:
        return int(pages[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')

    lst = []
    for item in items:
        lst.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'equip': item.find('div', class_='proposition_equip').get_text(strip=True),
            'link': HOST+item.find('a').get('href'),
            'info': item.find('div', class_='proposition_information').get_text(strip=True).replace('•', ', '),
            'price': item.find('span', 'green').get_text(strip=True),
            'city': item.find('svg', class_='svg-i16_pin').find_next('strong').get_text(strip=True),
        })
    return lst


def save_file(items, path):
    with open(path, 'w',  newline='', encoding='utf-8',) as file:

        writer = csv.writer(file, dialect='excel',)
        writer.writerow(['brand', 'style', 'link', 'info', 'price', 'city'])

        for item in items:
            writer.writerow([item['title'], item['equip'], item['link'], item['info'], item['price'], item['city']])


def parse():
    URL = input('Enter a URL code: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text) # get cnt of all pages
        for page in range(1, pages_count+1):
            print(f'Parsing page {page} of {pages_count} ...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))       #get all info about cars and put into list
        # print(cars)
        save_file(cars, FILE)
        print(f'Taked {len(cars)} cars')
        os.startfile(FILE)

    else:
        print("Error")



parse()
