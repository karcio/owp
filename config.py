import configparser

config = configparser.ConfigParser()


class configuration():

    def getDatabasePass(self):
        self.readConfig()
        return config.get('DB', 'DBPASSWORD')

    def getDatabaseUser(self):
        self.readConfig()
        return config.get('DB', 'DBUSER')

    def getDatabase(self):
        self.readConfig()
        return config.get('DB', 'DATABASE')

    def getPort(self):
        self.readConfig()
        return config.get('DB', 'PORT')

    def getHost(self):
        self.readConfig()
        return config.get('DB', 'HOST')

    def getCity(self):
        self.readConfig()
        return config.get('APP', 'CITY')

    def getApiKey(self):
        self.readConfig()
        return config.get('APP', 'API_KEY')

    def readConfig(self):
        property = config.read('./config.properties')

        return property
