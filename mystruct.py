import re


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_users(self):
        sql = "SELECT * FROM seoes_users"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
# Эта строка выводит результат в консоль, но обычно ее лучше убрать в продакшне
            print(res)
            return res
        except Exception:
            print("Ошибка чтения из БД")
            return []

    def create_user(self, role, name, number):
        try:
            self.__cur.execute("call insert_seoes_users(%d, %s, %s)"[
                                                    role, name, number])
            res = self.__cur.fetchall()
# Эта строка выводит результат в консоль, но обычно ее лучше убрать в продакшне
            print(res)
            return res
        except Exception:
            print("Ошибка добавления записи")
            return []


def validate_data_users(role, name, number):
    errors = {}
    if not role or not role.isdigit() or int(role) not in [1, 2]:
        errors['role'] = "Неверный формат роли (1 или 2)"
    if not name or len(name) > 100 or not re.fullmatch(
                r'[А-Яа-яЁё]+\s[А-Яа-яЁё]+\.[А-Яа-яЁё]\.', name):
        errors['name'] = "Неверный формат имени \
                (Имя Отчество, макс. 100 символов)"
    if not number or not re.fullmatch(r'8\d{10}', number):
        errors['number'] = "Неверный формат номера (8ХХХХХХХХХХ)"
    return errors


class Users:
    def __init__(self):
        self.users = []
        self.users_id = []

    def write_in(self, database):
        self.users = []
        for user in database.get_users():
            self.users.append(
                {
                    'user_id': int(user[0]),
                    'role_id': int(user[1]),
                    'user_full_name': user[2],
                    'user_number': user[3],
                }
            )
        print(self.users)
