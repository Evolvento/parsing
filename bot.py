import telebot
from db import DataAccessObject
from telebot import types


class Bot:
    dao = DataAccessObject()

    def __init__(self):
        self.bot = telebot.TeleBot('6626234697:AAE8PE28JcQcSpZQeDkHIKznngTJR-VvppE')

        @self.bot.message_handler(commands=['start'])
        def start(message):
            #self.dao.update()
            #self.dao.show_base()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            menu = types.KeyboardButton('Меню')
            markup.add(menu)
            self.bot.send_message(message.chat.id, 'Я собираю информацию с сайта lamoda.ru.\n'
                                                        'Обновление базы данных может занять какое-то время.\n'
                                                        '🔍 - начать поиск.', reply_markup=markup)
            main_buttons(message)

        def main_buttons(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start_search = types.KeyboardButton('🔍')
            markup.add(start_search)

        @self.bot.message_handler(func=lambda m: m.text == "🔍")
        def search(message):
            


    def run(self):
        self.bot.polling(none_stop=True, interval=0)


