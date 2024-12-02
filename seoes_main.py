import flask as f
# Flask, render_template, g, request, redirect, url_for, session, flash
import psycopg2
from mystruct import FDataBase, Users
from flask_sqlalchemy import SQLAlchemy
# import time


DATABASE = 'db_seoes'
DEBUG = True
USERNAME = 'postgres'
PASSWORD = 'root'
HOST = 'localhost'
PORT = 5433
SECRET_KEY = 'TARANTUL4.'


def connect_db():  # db.api
    conn = None
    try:
        conn = psycopg2.connect(database=DATABASE, user=USERNAME,
                                password=PASSWORD, host=HOST, port=PORT)
        return conn
    except Exception as e:
        print(e)
    if conn is None:
        print("None")


db = connect_db()
dbase = FDataBase(db)
users = Users()
app = f.Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = \
        "postgresql://postgres:root@localhost:5433/db_seoes"
db1 = SQLAlchemy(app)


# with app.app_context():


@app.route('/homepage')
def homepage():
    if 'user_id' not in f.session:
        return f.redirect(f.url_for('index'))
    return f.render_template('homepage.html', user_id=f.session["user_id"],
                             role_id=f.session['role_id'])


@app.route('/configs')
def about():
    return f.render_template('groups.html')


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    users.write_in(dbase)
    if f.request.method == 'POST':
        user_id = f.request.form['user_id']
        # Проверка пользователя
        for user in users.users:
            if int(user_id) == user['user_id']:
                f.session['user_id'] = user_id
                f.session['role_id'] = user['role_id']
                return f.redirect(f.url_for('homepage'))
        else:
            return f.jsonify({'error': 'Пользователь не найден'}), 404
    return f.render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
