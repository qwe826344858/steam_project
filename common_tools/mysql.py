import mysql
import mysql.connector

import sys
sys.path.append("/home/lighthouse/test_py/common_tools")
from commonConfig import CommonConfig

# default
# self.host = 'localhost'
# self.username = 'root'
# self.password = 'zoneslee'
# self.database = 'Buff_Project'
# self.connection = None

class DBHelper:
    host = ''
    username = ''
    password = ''
    database = ''
    connection = None
    table_name = ''

    def __init__(self, host, username, password, database, connection,table_name):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = connection
        self.table_name = table_name

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print("连接成功")
            return True
        except mysql.connector.Error as error:
            print("连接数据库时出错: {}".format(error))
            return False

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("断开连接")
        else:
            print("无连接,无需释放连接")

        return True

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return True,result

        except mysql.connector.Error as error:
            print("执行查询时出错: {}".format(error))
            return False,{}

    def execute_update(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("更新成功")
            return True

        except mysql.connector.Error as error:
            print("执行更新时出错: {}".format(error))
            self.connection.rollback()
            return False

    def execute_delete(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("删除成功")
            return True

        except mysql.connector.Error as error:
            print("执行删除时出错: {}".format(error))
            self.connection.rollback()
            return False

    def execute_insert(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("插入成功")
            return True

        except mysql.connector.Error as error:
            print("执行插入时出错: {}".format(error))
            self.connection.rollback()
            return False

    def _getLastSQL(self):
        return ""