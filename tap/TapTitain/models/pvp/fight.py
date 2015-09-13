import datetime
from managers.database_manager import db_Manager

__author__ = 'Mike'

class AttackerAndTargeter:
    def __init__(self,attackid,targetid):
        self.attackid = attackid
        self.targetid = targetid
        self.startTime = datetime.datetime.now()

    def refreshTime(self):
        self.startTime = datetime.datetime.now()

    def endRelation(self):
        pass








