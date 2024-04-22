class CommonConfig:
    mysql_host = 'localhost'
    mysql_username = 'root'
    mysql_password = 'zoneslee'
    mysql_database = 'Buff_Project'
    mysql_connection = None


    def getMysqlConfig(self):
        return {
            "host": self.mysql_host,
            "username": self.mysql_username,
            "password": self.mysql_password,
            "database": self.mysql_database,
            "connection": self.mysql_connection
        }
