# task-6

## Описание
Вебсервер, обслуживающий биржу криптовалют. Данные хранятся в базе postgres.

### Запуск сервера
* `set FLASK_APP=exchange.wsgi`
* `flask run`

### Запуск тестов
* `python -m pytest`

### Запуск линтера
* `flake8 exchange/`