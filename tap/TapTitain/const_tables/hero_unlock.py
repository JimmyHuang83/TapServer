from managers.database_manager import db_Manager

__author__ = 'Mike'
class HeroUnlockInfo:
    def __init__(self,data):
        self.order = data[0]
        self.cost = int(data[1])
        self.droplibs = data[2]
        self.modify = float(data[3])

class HeroUnlockTable:
    def __init__(self):
        self.tableData = {}

    def initTable(self):
        self.tableData.clear()
        tableName = "table_hero_unlock"
        fields = "orderid,cost,droplibs,modify"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = HeroUnlockInfo(oneData)
            self.tableData[item.order] = item

    def getHeroUnlockInfoByOrder(self,order):
        if order == 0:
            order = 1
        return self.tableData[order]

heroUnlockTable = HeroUnlockTable()