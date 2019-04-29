import pytest
from exchange.models import User, Currency, CurrencyStorage


def test_user_buy(mocker, currency, user, currency_storage):
    mocker.patch('exchange.models.Currency.get_currency', return_value=currency)
    mocker.patch('exchange.models.CurrencyStorage.get_currency_container', return_value=currency_storage)
    assert user.username == 'login'
    assert user.password == 'password'
    user.buy('Bitcoin')
    assert user.current_account == 900
    assert currency_storage.count == 1
    Currency.get_currency.assert_called_once_with("Bitcoin")
    CurrencyStorage.get_currency_container.assert_called_once_with('login', 'Bitcoin')
    user.buy('Bitcoin')
    assert user.current_account == 800
    assert currency_storage.count == 2


def test_user_buy_not_enough_currency(mocker, currency, user):
    mocker.patch('exchange.models.Currency.get_currency', return_value=currency)
    user.current_account = 99
    with pytest.raises(ValueError):
        user.buy('Bitcoin')
    assert user.current_account == 99


def test_user_sell(mocker, currency, user, currency_storage):
    mocker.patch('exchange.models.Currency.get_currency', return_value=currency)
    mocker.patch('exchange.models.CurrencyStorage.get_currency_container', return_value=currency_storage)
    currency_storage.count = 2
    user.sell('Bitcoin')
    assert user.current_account == 1080
    assert currency_storage.count == 1
    Currency.get_currency.assert_called_once_with("Bitcoin")
    CurrencyStorage.get_currency_container.assert_called_once_with('login', 'Bitcoin')
    user.sell('Bitcoin')
    assert user.current_account == 1160
    assert currency_storage.count == 0


def test_user_sell_not_enough_currency(mocker, currency_storage, user):
    mocker.patch('exchange.models.CurrencyStorage.get_currency_container', return_value=currency_storage)
    currency_storage.count = 0
    with pytest.raises(ValueError):
        user.sell('Bitcoin')
    assert user.current_account == 1000
