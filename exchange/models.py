from exchange.currencies import CURRENCIES
from exchange.wsgi import db
from uuid import uuid4


class Currency(db.Model):
    name = db.Column(db.String(80), primary_key=True, nullable=False)
    buy = db.Column(db.Integer)
    sell = db.Column(db.Integer)

    @staticmethod
    def fill_base():
        for currency_name in CURRENCIES:
            if Currency.get_currency(currency_name) is None:
                db.session.add(
                    Currency(name=currency_name, buy=CURRENCIES[currency_name][0], sell=CURRENCIES[currency_name][1]))
        db.session.commit()

    @staticmethod
    def get_currency(currency_name):
        return Currency.query.get(currency_name)


class CurrencyStorage(db.Model):
    id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    currency_name = db.Column(db.String(80), nullable=False)
    count = db.Column(db.Integer, default=0)

    @staticmethod
    def add_user(username):
        for currency_name in CURRENCIES:
            if CurrencyStorage.get_currency_container(username, currency_name) is None:
                db.session.add(CurrencyStorage(id=uuid4().hex, username=username,
                                               currency_name=currency_name))
        db.session.commit()

    @staticmethod
    def get_currency_container(username, currency_name):
        return CurrencyStorage.query.filter_by(username=username, currency_name=currency_name).first()


class User(db.Model):
    username = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    current_account = db.Column(db.Integer, default=1000)

    def buy(self, currency_name):
        currency = Currency.get_currency(currency_name)
        if self.current_account < currency.buy:
            raise ValueError
        CurrencyStorage.get_currency_container(self.username, currency_name).count += 1
        self.current_account -= currency.buy
        db.session.commit()

    def sell(self, currency_name):
        currency_container = CurrencyStorage.get_currency_container(self.username, currency_name)
        if currency_container.count <= 0:
            raise ValueError
        currency_container.count -= 1
        self.current_account += Currency.get_currency(currency_name).sell
        db.session.commit()

    @staticmethod
    def get_user(username):
        return User.query.get(username)
