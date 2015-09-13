from managers.database_manager import db_Manager

__author__ = 'Mike'
class PVPRankTimerReward:
    def __init__(self,data):
        self.fromNum = data[0]
        self.toNum = data[1]
        self.type = data[2]
        self.value = data[3]
        self.type1 = data[4]
        self.value1 = data[5]

class PVPRankTimerRewardTable:
    def __init__(self):
        self.tables = []


    def initData(self):
        self.tables.clear()
        tableName = "table_pvprank_timer_reward"
        fields = "fromRankNum,toRankNum,type,value,type1,value1"
        data = db_Manager.selectDataFromTable(tableName,fields)
        for itemData in data:
            item = PVPRankTimerReward(itemData)
            self.tables.append(item)

    def getRewardByRankNum(self,rankNum):
        for pvpRankTimerReward in self.tables:
            if rankNum >= pvpRankTimerReward.fromNum and rankNum <= pvpRankTimerReward.toNum:
                return pvpRankTimerReward

pvpRankTimerRewardTable = PVPRankTimerRewardTable()