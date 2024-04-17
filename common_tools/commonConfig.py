class CommonConfig:
    def getMysqlConfig(self):
        self.host = 'localhost'
        self.username = 'root'
        self.password = 'zoneslee'
        self.database = 'Buff_Project'
        self.connection = None
        return self
