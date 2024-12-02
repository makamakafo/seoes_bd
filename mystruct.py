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

