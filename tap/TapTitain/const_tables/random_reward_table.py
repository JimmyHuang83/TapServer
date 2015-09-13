from managers.database_manager import db_Manager

__author__ = 'Mike'


class RandomRewardManager:
    def __init__(self):
        self.tableData = {}

    def getValue(self,type):
        return  self.tableData.get(type,0)

    def initData(self):
        self.tableData.clear()
        tableName = "table_random_reward"
        fields = "type,power,`desc`,`value`"
        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            self.tableData[oneData[0]] = int(oneData[3])


randomRewardManager = RandomRewardManager()