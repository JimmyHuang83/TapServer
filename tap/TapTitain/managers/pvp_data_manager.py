import datetime
from config import Configration
from managers.database_manager import db_Manager

__author__ = 'Mike'
class PvpDataManager:
    def __init__(self):
        self.player2targets = {}
        self.fight2target = {}

    def addTargetList(self,attackerID, targetList): 
        self.player2targets[attackerID] = targetList


    def addFightStatus(self,playerid,targetid):

        self.fight2target[playerid] = targetid


    def fightFinished(self,playerid,targetid):
        s_target_id = self.fight2target.get(playerid,None)
        if s_target_id == None:
            return True
        del self.fight2target[playerid]
        return True

pvpDataManger = PvpDataManager()