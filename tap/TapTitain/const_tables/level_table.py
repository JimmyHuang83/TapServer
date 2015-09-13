from managers.database_manager import db_Manager

__author__ = 'Mike'
class LevelInfo:
    def __init__(self,data):
        self.id = data[0]
        self.monsterhp = int(data[1])
        self.monstercoins = int(data[2])
        self.bosshp = int(data[3])
        self.bosscoins = int(data[4])
        self.gem2coin = int(data[5])
        self.offlinegold = int(data[6])
        self.relivegold = int(data[7])
        self.eqmUpgradeAddCost = float(data[8])
        self.drawEquipCost = data[9]
        self.recycle = data[10]

class LevelTable:
    def __init__(self):
        self.tableData = {}

    def getItem(self,levelID):
        return  self.tableData[levelID]

    def initData(self):
        self.tableData.clear()
        tableName = "table_level"
        fields = "id,monsterhp,monstercoins,bosshp,bosscoins,ZsBuyGodRate,offlinegold,relivegold,eqm_upgrade_add_cost,draw_equip_cost,recycle"
        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = LevelInfo(oneData)
            self.tableData[item.id] = item

levelTable = LevelTable()