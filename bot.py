import telebot
from db import DataAccessObject
from telebot import types


class Bot:
    dao = DataAccessObject()

    def __init__(self):
        self.bot = telebot.TeleBot('token')

        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            menu = types.KeyboardButton('Меню')
            markup.add(menu)
            self.bot.send_message(message.chat.id, 'Я собираю информацию с сайта lamoda.ru.\n', reply_markup=markup)
            self.bot.register_next_step_handler(message, main_buttons)

        def main_buttons(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            search_card = types.KeyboardButton('🔍')
            markup.add(search_card)
            self.bot.send_message(message.chat.id, '🔍 - начать поиск\n'
                                                   'Обновление базы данных может занять какое-то время.', reply_markup=markup)

        @self.bot.message_handler(func=lambda m: m.text == "🔍")
        def search(message):
            self.dao.update()
            self.bot.send_message(message.chat.id, 'База данных обновилась, теперь вывести нужно')
            searching_buttons(message)

        def searching_buttons(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            next_card = types.KeyboardButton('Следующая')
            exit = types.KeyboardButton('Закончить поиск')
            markup.add(next_card, exit)

        @self.bot.message_handler(func=lambda m: m.text == "Следующая")
        def next(message):
            pass

        def show_card():
            pass

    def run(self):
        self.bot.polling(none_stop=True, interval=0)
