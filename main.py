import requests
from bs4 import BeautifulSoup
import csv

#Добавляем константы название файла csv, адрес страницы откуда достаем информацию и агент

CSV = 'eyes.csv'
HOST = 'https://chudodey.com/'
URL = 'https://chudodey.com/catalog/makiyazh/glaza'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

# Функция получения непосредственно кода html
def get_html(url, params=''):
    res = requests.get(url, headers=HEADERS, params=params)
    return res

# Так как необходимо перейти по внутренним ссылкам, то собираем список ссылок
def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='block-row product')
    links = []

    for item in items:
        links.append(item.find('div', class_='product__brief').find('a').get('href'))
    return links

# С каждой ссылки достаем html, аналогично фукции get_links() и с каждой страницы достаем
# необходимую нам информацию и помещаем ее в список словарей для удобства дальнейшей
# записи в файл
def get_content(html2):
    soup = BeautifulSoup(html2, 'html.parser')
    items = soup.find_all('div', id='product-block', class_='container')

    cards = []

    for item in items:
        characterics = []
        character = item.find_all('dt', class_='col-5')
        dates = []
        data = item.find_all('dd', class_='col-7')
        for i in data:
            dates.append(i.get_text(strip=True))

        for j in character:
            characterics.append(j.get_text(strip=True))

        block = dict(zip(characterics, dates))

        cards.append(
            {
                'наименование': item.find('h1', class_='product-detail__header').get_text(strip=True),
                'изображение': item.find('div', class_='d-flex').find('span').find('img').get('data-src'),
                'артикул': item.find('div', class_='invisible-line product-detail__articul').get_text(strip=True),
                'цена': item.find('div', class_='product-detail__price').get_text()
            }
        )
        cards[0].update(block)

    return cards

# Создем функцию записи в файл csv
def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Изображение', 'Артикул', 'Цена', 'Объем/вес',
                        'Тип', 'Бренд', 'Страна производства'])

        for item in items:

            writer.writerow([item['наименование'], item['изображение'], item['артикул'],
                            item['цена'], item['Объем/вес:'], item['Тип:'],
                            item['Бренд:'], item['Страна производства:']])


def parser():
    # Определяем количество пагинаций или необходимых страниц парсинга
    PAGENATION = int(input('Укажите количество страниц для парсинга: '))
    html = get_html(URL)

    # Оправляем запрос на сервер, если приходит ответ 200 то все OK, запускаем парсер
    if html.status_code == 200:
        links = []
        for page in range(1, PAGENATION+1):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            links.extend(get_links(html.text))

        cards = []
        for link in links:
            html2 = get_html(link)
            cards.extend(get_content(html2.text))
            save_doc(cards, CSV)
        print(cards)
    else:
        print('Error')

if __name__ == '__main__':
    parser()

