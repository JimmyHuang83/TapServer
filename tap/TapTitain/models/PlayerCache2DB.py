import random
import threading
import time
from managers.player_data_manager import playerDataManager

__author__ = 'Mike'
class SavePlayerDataThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.num = 0

    def run(self):
        while True:
            time.sleep(1)

            if( self. num >= 60):
                self.num = 0
            #do something
            playerDataManager.savePlayerData2DB(self.num)
            self.num += 1

    def Start(self):
        self.start()



savePlayerDataThread = SavePlayerDataThread()
