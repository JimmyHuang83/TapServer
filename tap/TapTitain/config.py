
__author__ = 'Mike'
class Configration:

    MAX_IDLE_TIME = 3# TOKEN will out date and player offline

    SERVER_ID = 0

    def __init__(self):
        self.serverDBList = []
        self.serverPortList = []
        self.serverDBList.append("TapTitain")
        self.serverPortList.append(16001)
        self.server_id = 1

    def getDBName(self):
        return self.serverDBList[Configration.SERVER_ID]

    def getPort(self):
        return self.serverPortList[Configration.SERVER_ID]

serverConfigManager = Configration()
SECRET_KEY = '81086f21b14cb137d256b9b078ff42e5'

