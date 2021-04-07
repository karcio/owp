import configparser

config = configparser.ConfigParser()


class configuration():
    
    def getApiKey(self):
        self.readConfig()
        return config.get('APP', 'API_KEY')


    def readConfig(self):
        property = config.read('./config.properties')

        return property
