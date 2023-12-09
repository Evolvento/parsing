import sqlite3
import requests
from bs4 import BeautifulSoup


class DataAccessObject:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.connection = sqlite3.connect('db.sqlite3', check_same_thread=False)
        self.dao = self.connection.cursor()
        self.dao.execute('''
            CREATE TABLE IF NOT EXISTS OurDataBase (
            href TEXT NOT NULL PRIMARY KEY,
            name TEXT,
            brand TEXT,
            price INTEGER,
            discount INTEGER,
            discount_price INTEGER,
            photo TEXT
            )
        ''')
        self.connection.commit()
        self.update()

    def create_card(self, href, name, brand, price, discount, discount_price, photo):
        self.dao.execute(
            'INSERT or REPLACE INTO OurDataBase(href, name, brand, price, discount, discount_price, photo)'
            ' VALUES(?, ?, ?, ?, ?, ?, ?)', (href, name, brand, price, discount, discount_price, photo))
        self.connection.commit()

    def get_discount(self):
        self.dao.execute('SELECT * FROM OurDataBase ORDER BY discount DESC')
        return self.dao.fetchall()

    def page_count(self) -> int:
        url = "https://www.lamoda.ru/c/4153/default-women/?is_new=1&sitelink=topmenuW&l=2&is_sale=1"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        cards = soup.find('span', class_="d-catalog-header__product-counter").text
        cards_all = 0
        for i in range(len(cards)):
            if cards[i] == ' ':
                cards_all = int(cards[:(i - 1)])
        card_on_page = 60
        return (cards_all - 1) // card_on_page + 1

    def update(self):
        #self.page_count()
        for count in range(1, 1):
            response = requests.get(f"https://www.lamoda.ru/c/4153/default-women/?is_new=1&sitelink=topmenuW&l=2&is_sale=1&page={count}")
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "lxml")
                data = soup.find_all("div", class_="x-product-card__card")
                for card in data:
                    href = "https://www.lamoda.ru" + card.find("a", class_="x-product-card__link x-product-card__hit-area").get("href")
                    name = card.find("div", class_="x-product-card-description__product-name").text
                    brand = card.find("div", class_="x-product-card-description__brand-name").text
                    price = int(card.find("span", class_="x-product-card-description__price-old").get_text().replace(' ', ''))
                    discount_price = int(card.find("span", class_="x-product-card-description__price-new x-product-card-description__price-WEB8507_price_no_bold").get_text().replace(' ', '')[:-1])
                    discount = 100 - (discount_price * 100 // price)
                    response_photo = requests.get(href)
                    if response_photo.status_code == 200:
                        soup = BeautifulSoup(response_photo.text, "lxml")
                        photo = 'https:' + soup.find('img', class_="x-premium-product-gallery__image").get('src')
                    self.create_card(href, name, brand, price, discount, discount_price, photo)

    def show_base(self):
        self.dao.execute('SELECT * FROM OurDataBase')
        result = self.dao.fetchall()
        for row in result:
            print(row)

