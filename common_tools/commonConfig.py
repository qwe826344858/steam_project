class CommonConfig:
    mysql_host = 'localhost'
    mysql_username = 'root'
    mysql_password = 'zoneslee'
    mysql_database = 'Buff_Project'

    # 日志保存路径
    save_path = '/home/lighthouse/LogInfo'

    # DB 配置
    def getMysqlConfig(self):
        return {
            "host": self.mysql_host,
            "username": self.mysql_username,
            "password": self.mysql_password,
            "database": self.mysql_database,
        }

    # 获取保存日志的文件路径
    def _getLogSavePath(self):
        return self.save_path


    # 获取日志配置信息
    @staticmethod
    def getLogConfig():
        config = {
            'save_path': CommonConfig._getLogSavePath()
        }

        return config
