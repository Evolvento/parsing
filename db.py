import sqlite3


class DataAccessObject:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.connection = sqlite3.connect('db.sqlite3')
        self.dao = self.connection.cursor()
        self.dao.execute('''
            CREATE TABLE IF NOT EXISTS OurDataBase (
            href TEXT NOT NULL PRIMARY KEY,
            name TEXT,
            brand TEXT,
            price INTEGER,
            discount_price INTEGER,
            information TEXT,
            photo TEXT
            )
        ''')
        self.connection.commit()

    def create_card(self, href, name, brand, price, discount_price, information, photo):
        self.dao.execute(
            'INSERT or REPLACE INTO OurDataBase(href, name, brand, price, discount_price, information, photo) VALUES(?, ?, ?, ?, ?, ?, ?)',
            (href, name, brand, price, discount_price, information, photo))
        self.connection.commit()

    def show_base(self):
        self.dao.execute('SELECT * FROM OurDataBase')
        result = self.dao.fetchall()
        for row in result:
            print(row)

