from functools import wraps

from flask import Response, redirect, render_template, request, url_for, flash, abort

from .models import User, Currency, CurrencyStorage
from .wsgi import app, db

db.create_all()

Currency.fill_base()


def check_auth(username, password):
    user = User.get_user(username)
    if user is not None:
        return user.password == password
    return True


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or auth is None or not check_auth(auth.username, auth.password):
            return authenticate()
        if User.get_user(auth.username) is None:
            db.session.add(User(username=auth.username, password=auth.password))
        CurrencyStorage.add_user(auth.username)
        db.session.commit()
        return f(*args, **kwargs)

    return decorated


def get_login():
    auth = request.authorization
    return auth.username if auth is not None else None


@app.route('/')
@requires_basic_auth
def index():
    return redirect(url_for('authed_index', login=get_login()))


@app.route('/<login>')
@requires_basic_auth
def authed_index(login):
    if get_login() != login:
        abort(404)
    return render_template('index.html', user=User.get_user(login), currencies=Currency.query,
                           currency_storage=CurrencyStorage.query.filter_by(username=login))


@app.route('/<login>/buy/<currency_name>')  # pragma: no cover
def buy(login, currency_name):
    try:
        User.get_user(login).buy(currency_name)
    except ValueError:
        flash('You have not enough money')
    return redirect(url_for('authed_index', login=login))


@app.route('/<login>/sell/<currency_name>')
def sell(login, currency_name) -> Response:
    try:
        User.get_user(login).sell(currency_name)
    except ValueError:
        flash('You have not enough currency')
    return redirect(url_for('authed_index', login=login))
