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
    @classmethod
    def _getLogSavePath(cls):
        return cls.save_path


    # 获取日志配置信息
    @staticmethod
    def getLogConfig():
        config = {
            'save_path': CommonConfig._getLogSavePath(),
            'distributed': True,
            'retry_max': 5,          # 重试的最大次数(单台服务器)
            'retry_time_out': 60,   # 重试后最大超时的时间(分布式)
        }

        return config
