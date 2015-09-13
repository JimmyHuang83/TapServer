from managers.database_manager import db_Manager

__author__ = 'Mike'

class EquipmentUpgradeConstInfo:
    def __init__(self,data):
        self.level = data[0]
        self.baseCost = float(data[1])
        self.buffAdd = float(data[2])

class EquipmentUpgradeTable:
    def __init__(self):
        self.tableData = {}

    def initTable(self):
        self.tableData.clear()
        tableName = "table_equipment_levelup"
        fields = "level,costbase,buffadd"

        data = db_Manager.selectDataFromTable(tableName,fields)
        for oneData in data:
            item = EquipmentUpgradeConstInfo(oneData)
            self.tableData[item.level] = item

    def getEuipmentLevelUpInfo(self,level):
        return  self.tableData.get(level)


equipmentUpgradeTable = EquipmentUpgradeTable()