import requests
from bs4 import BeautifulSoup
from db import DataAccessObject


dao = DataAccessObject()
#response = requests.get("https://www.lamoda.ru/c/4153/default-women/?is_new=1&sitelink=topmenuW&l=2&is_sale=1")
# = BeautifulSoup(response.text, "lxml")
#data = soup.find("div", class_="_info_7g9n8_20")
#print(soup)
#pages = data.find("div", class_="_info_7g9n8_20").text
#card_on_page = ''
#for i in range(len(pages)):
#    if pages[i].isdigit():
#        card_on_page += pages[i]
#card_all = int(card_on_page[len(card_on_page):])
#card_on_page = int(card_on_page)
#number_pages = (card_all - 1)//card_on_page + 1
number_pages = 3

for count in range(1, number_pages + 1):
    response = requests.get(f"https://www.lamoda.ru/c/4153/default-women/?is_new=1&sitelink=topmenuW&l=2&is_sale=1&page={count}")
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.find_all("div", class_="x-product-card__card")
    for card in data:
        href = "https://www.lamoda.ru" + card.find("a", class_="x-product-card__link x-product-card__hit-area").get("href")
        name = card.find("div", class_="x-product-card-description__product-name").text
        brand = card.find("div", class_="x-product-card-description__brand-name").text
        price = card.find("span", class_="x-product-card-description__price-old").get_text()
        discount_price = card.find("span", class_="x-product-card-description__price-new x-product-card-description__price-WEB8507_price_no_bold").get_text()
        information = "gg"
        photo = "wp"
        dao.create_card(href, name, brand, price, discount_price, information, photo)
dao.show_base()
