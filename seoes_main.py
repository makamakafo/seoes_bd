import flask as f
# Flask, render_template, g, request, redirect, url_for, session, flash
import psycopg2
from mystruct import FDataBase, Users, validate_data_users
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Sequence
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


class Group(db1.Model):
    __tablename__ = 'seoes_groups'  # Указываем название таблицы

    group_id = db1.Column(Integer, Sequence('group_id_seq'), primary_key=True)
    group_name = db1.Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Group(group_id={self.group_id}, \
                    group_name='{self.group_name}')>"


@app.route('/homepage')
def home_page():
    if 'user_id' not in f.session:
        return f.redirect(f.url_for('index'))
    return f.render_template('homepage.html', user_id=f.session["user_id"],
                             role_id=f.session['role_id'])


@app.route('/groups')
def groups_page():
    if 'user_id' not in f.session:
        return f.redirect(f.url_for('index'))
    groups = Group.query.all()
    print(groups)
    return f.render_template('groups.html', groups=groups,
                             user_id=f.session["user_id"],
                             role_id=f.session['role_id'])


@app.route('/users', methods=['GET', 'POST'])
def users_page():
    if 'user_id' not in f.session:
        return f.redirect(f.url_for('index'))
    if f.request.method == 'POST':
        role = f.request.form['role']
        name = f.request.form('f_name')
        number = f.request.form('number')
        errors = validate_data_users(role, name, number)
        if errors:
            return f.jsonify({'errors': errors}), 400
        dbase.create_user(role, name, number)  # Замените на вашу функцию добавления в БД
        users.write_in(dbase)
        return f.jsonify({'message': 'Данные успешно добавлены'}), 201
    return f.render_template('users.html', users=users.users,
                             user_id=f.session["user_id"],
                             role_id=f.session['role_id'])


@app.route('/search_data')
def search_data_page():
    if 'user_id' not in f.session:
        return f.redirect(f.url_for('index'))
    groups = Group.query.all()
    return f.render_template('search_data.html', group=groups,
                             user_id=f.session["user_id"],
                             role_id=f.session['role_id'])


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
                return f.redirect(f.url_for('home_page'))
        else:
            return f.jsonify({'error': 'Пользователь не найден'}), 404
    return f.render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='192.168.31.179', port=5000)
