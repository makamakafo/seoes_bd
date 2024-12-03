import re
import random as rnd


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_users(self):
        sql = "SELECT * FROM seoes_users"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res
        except Exception:
            print("Ошибка чтения из БД")
            return []

    def create_user(self, role, name, number):
        try:
            self.__cur.execute("call insert_seoes_users(%s, %s, %s)", (
                                                    int(role), name, number))
            self.__cur.connection.commit()
        except Exception as e:
            print(f"Ошибка добавления записи: {e}")
            return False
        return True

    def delete_user(self, user_id):
        try:
            id = str(user_id)
            self.__cur.execute("call delete_seoes_users(%s)", (id,))
            self.__cur.connection.commit()
        except Exception as e:
            print(f"Ошибка удаления записи: {e}")
            return False
        return True
    
    def get_memberships(self):
        sql = "SELECT * FROM user_group_memberships"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res
        except Exception:
            print("Ошибка чтения из БД")
            return []
        
    def get_configs(self):
        try:
            self.__cur.execute('select * from seoes_config_view order by "ID Конфига"')
            res = self.__cur.fetchall()
            return res
        except Exception:
            print("Ошибка чтения из БД")
            return []
        
    def get_search_data(self, id):
        try:
            self.__cur.execute("select * from get_config_search_data(%s)", (id,))
            res = self.__cur.fetchall()
            print(res)
            return res
        except Exception:
            print("Ошибка чтения из БД")
            return []
        
    def create_config(self, group_id, host_user_id, site_name, url, access_token):
        try:
            self.__cur.execute("call insert_seoes_config(%s, %s, %s, %s, %s)", (
                int(group_id), int(host_user_id), site_name, url, access_token))
            self.__cur.connection.commit()
        except Exception as e:
            print(f"Ошибка добавления записи: {e}")
            return False
        return True

    def delete_config(self, config_id):
        try:
            config_id = str(config_id)
            self.__cur.execute("call delete_seoes_config(%s)", (config_id,))
            self.__cur.connection.commit()
        except Exception as e:
            print(f"Ошибка удаления записи: {e}")
            return False
        return True
    
    def update_config(self, config_id, group_id, host_user_id, site_name, url, access_token):
        try:
            config_id = str(config_id)
            self.__cur.execute("call update_seoes_config(%s, %s, %s, %s, %s, %s)", (
                config_id, group_id, host_user_id, site_name, url, access_token))
            self.__cur.connection.commit()
        except Exception as e:
            print(f"Ошибка удаления записи: {e}")
            return False
        return True
    
    def create_search_data(self, config_id):
        average_position = rnd.randint(1, 100)
        click_rate = rnd.randint(100, 1000)
        number_of_view = rnd.randint(100, 1000)
        try:
            config_id = str(config_id)
            self.__cur.execute("call insert_seoes_search_data(%s, %s, %s, %s)", (
                int(config_id), int(average_position), int(click_rate), int(number_of_view)))
            #res = self.__cur.fetchall()
            #print(res)
            self.__cur.connection.commit()
        except Exception as e:
            print(f"Ошибка добавления записи: {e}")
            self.__db.rollback()
            return False
        return True
    
    def delete_seoes_search_data(self, search_id):
        try:
            search_id = str(search_id)
            self.__cur.execute("call delete_seoes_search_data(%s)", (search_id,))
            self.__cur.connection.commit()
        except Exception as e:
            print(f"Ошибка удаления записи: {e}")
            self.__db.rollback()
            return False
        return True


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


class Users_Group_membership:
    def __init__(self):
        self.users_group = []


def write_in_membership(Us_Gr, database):
    Us_Gr.users_group = []
    for membership in database.get_memberships():
        Us_Gr.users_group.append([membership[0], membership[1]])
    print(Us_Gr.users_group)


class Configs:
    def __init__(self):
        self.configs_row = []


class Search_data:
    def __init__(self):
        self.data_row = []


def write_in_configs(configs, database):
    configs.configs_row = []
    for config in database.get_configs():
        configs.configs_row.append(list(config))
    print(configs.configs_row)


def write_in_search_data(search_data, database, config_id):
    search_data.data_row = []
    for config in database.get_search_data(config_id):
        search_data.data_row.append(list(config))
    print(search_data.data_row)
