from managers.database_manager import db_Manager

__author__ = 'Mike'
class UpgradeInfoH:
    def __init__(self,data):
        self.level = data[0]
        self.cost = int(data[1])
        self.effadd = int(data[2])
        self.effValue = 0
        self.PVP_hp = int(data[3])


class HeroUpgradeTable:
    def __init__(self):
        self.tableData = {}


    def initData(self):
        self.tableData.clear()
        tableName = "table_hero_upgrade"
        fields = "level,cost,effadd,PVP_hp"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = UpgradeInfoH(oneData)
            self.tableData[item.level] = item
            if item.level == 1:
                item.effValue = item.effadd
            else:
                lastValue = self.tableData[item.level - 1].effValue
                value = lastValue + item.effadd
                item.effValue = value

    def getHeroUpgradeInfo(self,level):
        return self.tableData[level]

heroUpgradeTable = HeroUpgradeTable()