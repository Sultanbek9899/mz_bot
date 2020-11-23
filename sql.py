import sqlite3


class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def get_user_info(self, user_id):
        """Получаем всех активных подписчиков бота"""
        query=f"""SELECT * FROM `hospi_info` WHERE `user_id` = '{user_id}' """
        with self.connection:
            return self.cursor.execute(query).fetchone()

    def user_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute("""SELECT * FROM `hospi_info` WHERE `user_id`=? """, (user_id,)).fetchall()
            return bool(len(result))

    def add_new_user(self, user_id, field, text):
        """Добавляем нового подписчика"""
        query = f"""INSERT INTO `hospi_info` (`user_id`, `{field}` ) VALUES( '{user_id}', '{text}' )"""
        with self.connection:
            return self.cursor.execute(query)

    def create_table(self):
        with self.connection:
            query = """CREATE TABLE IF NOT EXISTS hospi_info(`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,`user_id` INTEGER , `full_name` TEXT, `pin` INTEGER, `relationship` TEXT, `phone_number` TEXT, `patient_name` TEXT, `date_of_birth` TEXT, `hospitalization_date` TEXT, `hospitalization_place` TEXT) """
            self.cursor.execute(query)

    def table_exist(self):
        c = self.cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='hospi_info' ''')
        # if the count is 1, then table exists
        if c.fetchone()[0] == 1:
            print('Table exists.')
            return True
        else:
            print('Table does not exist.')
            return False

    def update_info(self, user_id, field, text):
        """Обновляем статус подписки пользователя"""
        query=f"""UPDATE `hospi_info` SET `{field}`='{text}' WHERE `user_id` = '{user_id}' """
        with self.connection:
            return self.cursor.execute(query)

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()