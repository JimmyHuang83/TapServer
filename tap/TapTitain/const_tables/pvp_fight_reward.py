from managers.database_manager import db_Manager

__author__ = 'Mike'
class PvpReward:
    def __init__(self,data):
        self.result = data[0]
        self.type = data[1]
        self.value = data[2]



class PvpFightRewardTable:
    def __init__(self):
        self.tableData = {}

    def initData(self):
        self.tableData.clear()
        tableName = "table_pvp_fight_reward"
        fields = "result,reward_type,reward_value"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            result = oneData[0]
            type = oneData[1]
            value = oneData[2]
            pvpReward = PvpReward(oneData)
            l = self.tableData.get(result,None)
            if l == None:
                self.tableData[result] = []
            self.tableData[result].append(pvpReward)
    def getPvpFightRewardByResult(self,result):
        return self.tableData.get(result,None)

pvpFightRewardTable = PvpFightRewardTable()