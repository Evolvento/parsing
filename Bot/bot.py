import telebot
from db import DataAccessObject
from telebot import types


class Bot:
    dao = DataAccessObject()
    cards = []

    def __init__(self):
        self.bot = telebot.TeleBot('token')
        self.iterator = 0

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.dao.update()
            self.cards = self.dao.get_cards()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            menu = types.KeyboardButton('Меню')
            markup.add(menu)
            self.bot.send_message(message.chat.id, 'Я собираю информацию с сайта lamoda.ru.\n', reply_markup=markup)
            self.bot.register_next_step_handler(message, main_buttons)

        @self.bot.message_handler(func=lambda m: m.text == "Меню")
        def main_buttons(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            search_card = types.KeyboardButton('Начать поиск')
            update_button = types.KeyboardButton('Обновить данные')
            markup.add(search_card, update_button)
            self.bot.send_message(message.chat.id, 'Обновление базы данных может занять какое-то время.', reply_markup=markup)

        @self.bot.message_handler(func=lambda m: m.text == "Обновить данные")
        def search(message):
            self.dao.update()
            self.bot.send_message(message.chat.id, 'Обновление завершено')
            main_buttons(message)

        @self.bot.message_handler(func=lambda m: m.text == "Начать поиск")
        def search(message):
            #self.dao.update()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            next_card_button = types.KeyboardButton('Следующая')
            exit_button = types.KeyboardButton('Закончить поиск')
            markup.add(next_card_button, exit_button)
            self.bot.send_message(message.chat.id, 'Выберите команду', reply_markup=markup)

        @self.bot.message_handler(func=lambda m: m.text == 'Следующая')
        def next_card(message):
            show_card(message)
            search(message)

        @self.bot.message_handler(func=lambda m: m.text == 'Закончить поиск')
        def exit_search(message):
            self.iterator = 0
            main_buttons(message)

        def show_card(message):
            href = self.cards[self.iterator]
            discount = self.dao.det_discount(href)
            self.iterator += 1
            self.bot.send_message(message.chat.id, f'Скидочка: {str(discount)}%\n {str(href)}')

    def run(self):
        self.bot.polling(none_stop=True, interval=0)


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
