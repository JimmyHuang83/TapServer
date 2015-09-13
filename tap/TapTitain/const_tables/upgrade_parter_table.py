from managers.database_manager import db_Manager

__author__ = 'Mike'
class UpgradeInfoP:
    def __init__(self,data):
        self.level = data[0]
        self.cost = int(data[1])
        self.effadd = int(data[2])
        self.effValue = 0

class PartnerUpgradeTable():
    def __init__(self):
        self.tableData = {}

    def initData(self):
        self.tableData.clear()
        tableName = "table_parter_upgrade"
        fields = "level,cost,effadd"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = UpgradeInfoP(oneData)
            self.tableData[item.level] = item
            if item.level == 1:
                item.effValue = item.effadd
            else:
                lastValue = self.tableData[item.level - 1].effValue
                value = lastValue + item.effadd
                item.effValue = value


    def GetPartnerUpgradeInfo(self,level):
        return  self.tableData[level]

partnerUpgradeTable = PartnerUpgradeTable()