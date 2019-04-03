import pytest

from exchange.views import User


class CurrencyTest:
    def __init__(self):
        self.buy = 100
        self.sell = 80
        self.name = 'Bitcoin'


class CurrencyStorageTest:
    def __init__(self):
        self.count = 0
        self.username = 'login'
        self.currency_name = 'Bitcoin'


@pytest.fixture
def currency():
    return CurrencyTest()


@pytest.fixture
def user():
    return User(username='login', password='password', current_account=1000)


@pytest.fixture
def currency_storage():
    return CurrencyStorageTest()
