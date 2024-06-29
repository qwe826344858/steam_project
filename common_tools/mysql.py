import mysql
import mysql.connector

import sys
sys.path.append("/home/lighthouse/test_py/common_tools")
from commonConfig import CommonConfig
from common_tools.loggerHelper import Logger

# 初始化日志
Logger.init()
# default
# self.host = 'localhost'
# self.username = 'root'
# self.password = 'zoneslee'
# self.database = 'Buff_Project'
# self.connection = None

class DBHelper:
    # DB 连接参数
    host = ''
    username = ''
    password = ''
    database = ''
    connection = None

    # 数据库表名
    table_name = ''

    instance = None     # 单例 防止重复创建

    def __new__(cls, host, username, password, database, table_name):
        Logger.info("DBHelper 创建对象")
        # 检查实例是否已经存在，如果存在，则直接返回该实例
        if not DBHelper.instance:
            DBHelper.instance = super().__new__(cls)
        return DBHelper.instance

    def __init__(self, host, username, password, database,table_name):
        Logger.info("DBHelper 初始化")
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.table_name = table_name
        self.connect()


    def __del__(self):
        self.disconnect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database
            )
            Logger.info("连接成功")
            return True
        except mysql.connector.Error as error:
            Logger.info("连接数据库时出错: {}".format(error))
            return False

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()

        return True

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = self._TranRawData2DictList(cursor)
            return True,result

        except mysql.connector.Error as error:
            Logger.info("执行查询时出错: {}".format(error))
            return False,{}

    def execute_update(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            Logger.info("更新成功")
            return True

        except mysql.connector.Error as error:
            Logger.info("执行更新时出错: {}".format(error))
            self.connection.rollback()
            return False

    def execute_delete(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            Logger.info("删除成功")
            return True

        except mysql.connector.Error as error:
            Logger.info("执行删除时出错: {}".format(error))
            self.connection.rollback()
            return False

    def execute_insert(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            Logger.info("插入成功")
            return True

        except mysql.connector.Error as error:
            Logger.info("执行插入时出错: {}".format(error))
            self.connection.rollback()
            return False

    def _getLastSQL(self):
        return ""


    def _TranRawData2DictList(self,cursor):
        column_names = [desc[0] for desc in cursor.description]
        rawData = cursor.fetchall()
        # 转换为键值对列表
        result_dict_list = []
        for row in rawData:
            row_dict = {}
            for i, column_name in enumerate(column_names):
                row_dict[column_name] = row[i]
            result_dict_list.append(row_dict)
        return result_dict_list