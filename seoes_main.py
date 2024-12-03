import flask as f
# Flask, render_template, g, request, redirect, url_for, session, flash
import psycopg2
from mystruct import FDataBase, Users, validate_data_users, \
    Users_Group_membership, write_in_membership, Configs, write_in_configs, \
    Search_data, write_in_search_data
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
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
memberships = Users_Group_membership()
configs = Configs()
search_data = Search_data()
app = f.Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = \
        "postgresql://postgres:root@localhost:5433/db_seoes"
db1 = SQLAlchemy(app)


class Group(db1.Model):
    __tablename__ = 'seoes_groups'  # Указываем название таблицы

    group_id = db1.Column(Integer, primary_key=True)
    group_name = db1.Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Group(group_id={self.group_id}, \
                    group_name='{self.group_name}')>"


@app.route('/homepage', methods=['GET', 'POST', 'DELETE', 'PUT'])
def home_page():
    if 'user_id' not in f.session:
        return f.redirect(f.url_for('index'))
    write_in_membership(memberships, dbase)
    write_in_configs(configs, dbase)
    if f.request.method == 'POST':
        group_id = f.request.form['group_id']
        host_user_id = f.request.form['host_user_id']
        site_name = f.request.form['site_name']
        url = f.request.form['url']
        access_token = f.request.form['access_token']
        if dbase.create_config(group_id, host_user_id, site_name, url, access_token):  # Замените на вашу функцию добавления в БД
            write_in_configs(configs, dbase)
            return f.jsonify({'response': "good create user"}), 200
        else:
            return f.jsonify({'errors': "Ошибка добавления"}), 500
    if f.request.method == 'DELETE':
        id = f.request.form['config_id']
        try:
            if dbase.delete_config(id):
                users.write_in(dbase)
                return f.jsonify({'response': "good delete"}), 200
            else:
                return f.jsonify({'message': 'Ошибка удаления'}), 500
        except ValueError:
            return f.jsonify({'message': 'Неверный тип данных'}), 500
    if f.request.method == 'PUT':
        id = f.request.form['config_id']
        group_id = f.request.form['group_id']
        host_user_id = f.request.form['host_user_id']
        site_name = f.request.form['site_name']
        url = f.request.form['url']
        access_token = f.request.form['access_token']
        if dbase.update_config(id, group_id, host_user_id, site_name, url, access_token):  # Замените на вашу функцию добавления в БД
            write_in_configs(configs, dbase)
            return f.jsonify({'response': "good update user"}), 200
        else:
            return f.jsonify({'errors': "Ошибка обновления"}), 500
    return f.render_template('homepage.html', user_id=int(f.session['user_id']),
                             configs=configs.configs_row,
                             role_id=f.session['role_id'])


@app.route('/groups', methods=['GET', 'POST', 'DELETE'])
def groups_page():
    if 'user_id' not in f.session:
        return f.redirect(f.url_for('index'))
    groups = Group.query.all()
    return f.render_template('groups.html', groups=groups,
                             memberships=memberships,
                             users=users.users,
                             user_id=f.session["user_id"],
                             role_id=f.session['role_id'])


@app.route('/homepage/<int:config_id>', methods=['GET', 'POST', 'DELETE'])
def search_data_page(config_id):
    if 'user_id' not in f.session:
        return f.redirect(f.url_for('index'))
    write_in_search_data(search_data, dbase, int(config_id))
    if f.request.method == 'POST':
        if dbase.create_search_data(config_id):  # Замените на вашу функцию добавления в БД
            write_in_search_data(search_data, dbase, int(config_id))
            return f.jsonify({'response': "good create user"}), 200
        else:
            write_in_search_data(search_data, dbase, int(config_id))
            return f.jsonify({'errors': "Ошибка добавления"}), 500
    if f.request.method == 'DELETE':
        id = f.request.form['search_id']
        try:
            if dbase.delete_seoes_search_data(id):
                write_in_search_data(search_data, dbase, int(config_id))
                return f.jsonify({'response': "good delete"}), 200
            else:
                return f.jsonify({'message': 'Ошибка удаления'}), 500
        except ValueError:
            return f.jsonify({'message': 'Неверный тип данных'}), 500
    return f.render_template('search_data_page.html',
                             search_data=search_data.data_row,
                             user_id=f.session["user_id"],
                             role_id=f.session['role_id'], config_id=config_id)


@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def users_page():
    if 'user_id' not in f.session:
        print(2)
        return f.redirect(f.url_for('index'))
    if f.request.method == 'POST':
        # f.session['user_id'] = user_id
        # f.session['role_id'] = user['role_id']
        role = f.request.form['role_id']
        name = f.request.form['user_full_name']
        number = f.request.form['user_number']
        errors = validate_data_users(role, name, number)
        if errors:
            return f.jsonify({'errors': errors}), 500
        if dbase.create_user(role, name, number):  # Замените на вашу функцию добавления в БД
            users.write_in(dbase)
            return f.jsonify({'response': "good create user"}), 200
        else:
            print('ошибка добавления')
    if f.request.method == 'DELETE':
        id = f.request.form['Id']
        try:
            if dbase.delete_user(id):
                users.write_in(dbase)
                return f.jsonify({'response': "good delete"}), 200
            else:
                return f.jsonify({'message': 'Ошибка удаления'}), 500
        except ValueError:
            return f.jsonify({'message': 'Неверный тип данных'}), 500

    return f.render_template('users.html', users=users.users,
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
    app.run(debug=True, host='192.168.56.1', port=5000)
