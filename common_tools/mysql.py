import mysql
from commonConfig import CommonConfig

# default
# self.host = 'localhost'
# self.username = 'root'
# self.password = 'zoneslee'
# self.database = 'Buff_Project'
# self.connection = None

class DBHelper:
    def __init__(self, host, username, password, database):
        self = CommonConfig.getMysqlConfig(self)
        if self.host is None or self.username is None or self.password is None or self.password is None :
            self.host = host
            self.username = username
            self.password = password
            self.database = database
            self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("连接成功")

        except mysql.connector.Error as error:
            print("连接数据库时出错: {}".format(error))

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("断开连接")

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result

        except mysql.connector.Error as error:
            print("执行查询时出错: {}".format(error))

    def execute_update(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("更新成功")

        except mysql.connector.Error as error:
            print("执行更新时出错: {}".format(error))
            self.connection.rollback()

    def execute_delete(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("删除成功")

        except mysql.connector.Error as error:
            print("执行删除时出错: {}".format(error))
            self.connection.rollback()

    def execute_insert(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("插入成功")

        except mysql.connector.Error as error:
            print("执行插入时出错: {}".format(error))
            self.connection.rollback()