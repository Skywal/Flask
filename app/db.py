from typing import List

import pymysql
from pymysql.cursors import DictCursor
from contextlib import closing
from config import db_config


class SQLDao(object):
    def __init__(self):
        self.general_connection = None

    def make_connection(self):
        self.general_connection = pymysql.connect(host=db_config['host'],
                                                  user=db_config['user'],
                                                  password=db_config['password'],
                                                  db=db_config['db'],
                                                  cursorclass=DictCursor
                                                  )
        return self.general_connection

    def get_all_table_names(self) -> List[str]:
        self.make_connection()

        with closing(self.general_connection) as con:
            cursor = con.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'framework';")
            result = cursor.fetchall()

            try:
                result = [i['TABLE_NAME'] for i in result]
            except:
                return []

        return result

    def get_table_content(self, table_name) -> List[dict]:
        self.make_connection()

        with closing(self.general_connection) as con:
            cursor = con.cursor()
            cursor.execute(f"SELECT * FROM {table_name};")
            result = cursor.fetchall()
            # print(result)
            return result

    def get_table_column_name(self, table_name) -> List[str]:
        self.make_connection()

        with closing(self.general_connection) as con:
            cursor = con.cursor()
            cursor.execute(
                f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'framework' AND TABLE_NAME = '{table_name}';")
            result = cursor.fetchall()
            # print(result)
            result = [i['COLUMN_NAME'] for i in result]
            # print(result)
            return result

    def find_user_names_by_id(self, user_id: list):
        self.make_connection()

        result = []
        with closing(self.general_connection) as conn:
            with conn.cursor() as cursor:
                for item in user_id:
                    str_command = "SELECT * FROM `{0}` WHERE {1} = %s".format('user', 'id_telegram')

                    cursor.execute(str_command, item)
                    result.append(cursor.fetchall())

                result = [item[-1] for item in result]
                # print(result)
                return result if len(result) > 0 else []
        return []

    def get_creators_from_all_questionnaire_table(self):
        self.make_connection()

        users = []
        with closing(self.general_connection) as conn:
            with conn.cursor() as cursor:
                str_command = "SELECT `id_user` FROM framework.all_polls;"

                cursor.execute(str_command)
                result = cursor.fetchall()

                print(result)

                result = [item['id_user'] for item in result]
                result = set(result)

                for item in result:
                    str_command = "SELECT `name_telegram`, `last_name_telegram`, `login_telegram`, `id_telegram` FROM framework.user WHERE `id_telegram` = %s;"

                    cursor.execute(str_command, item)
                    res = cursor.fetchall()[-1]
                    # print(res)
                    users.append(res)
                    # users.append({
                    #     'name_telegram': res[0],
                    #     'last_name_telegram': res[1],
                    #     'login_telegram': res[2],
                    #     'id_telegram': res[3],
                    # })

        return users

    def get_all_questionnaire_general_info(self):
        self.make_connection()

        with closing(self.general_connection) as conn:
            with conn.cursor() as cursor:
                str_command = "SELECT * FROM framework.all_polls;"

                cursor.execute(str_command)
                res = cursor.fetchall()
                # print(res)
                return res


if __name__ == "__main__":
    # print(get_all_table_names())
    # print(get_creators_from_all_questionnaire_table())
    conn = SQLDao()

    # conn.get_all_questionnaire_general_info()

    # conn.get_creators_from_all_questionnaire_table()
    # print(conn.find_user_names_by_id([901006354, 988610058]))

    # print(conn.get_table_column_name('all_polls'))
    # print(conn.get_table_content('bot_launch'))
    # print(conn.get_all_table_names())
